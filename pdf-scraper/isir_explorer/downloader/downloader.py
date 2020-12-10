import os
import json
import asyncio
import aiohttp
import aiofiles
import logging
from databases import Database
from datetime import datetime
from .errors import DownloaderException, TooManyRetries
from ..webservice.isir_models import IsirUdalost
from ..scraper.isir_scraper import IsirScraper
from ..dbimport.db_import import DbImport

class Downloader:

    def __init__(self, config):
        self.config = config
        self.db = Database(self.config['db.dsn'], min_size=10, max_size=20)
        self.tasks = []
        self.transaction_lock = asyncio.Lock()

        self.tmp_base = self.config['tmp_dir'].rstrip("/")
        self.tmp_path = self.tmp_base + "/pdf"
        self.log_path = self.tmp_base + "/log"
        self.tmpDir()

    def tmpDir(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    def schedule_task(self, session, row):
        request_task = DocumentTask(self, session, row)
        request_task.task = asyncio.create_task(request_task.run())
        self.tasks.append(request_task)

    async def cancel_tasks(self):
        for download_task in self.tasks:
            try:
                download_task.task.cancel()
                await download_task.task
            except asyncio.CancelledError:
                print(f"{download_task} cancelled")
            except Exception as e:
                print(f"{download_task} cancellation problem: {e}")
        self.tasks = []

    async def fetchRows(self, session):
        query = """
        SELECT * FROM isir_udalost
            WHERE
                priznakanvedlejsiudalost=false AND
                precteno IS NULL AND
                typudalosti = :typudalosti
        UNION
        SELECT iu2.* FROM isir_udalost iu
            JOIN isir_udalost iu2
            ON (
                iu.spisovaznacka = iu2.spisovaznacka AND
                iu.oddil = iu2.oddil AND
                iu.cislovoddilu = iu2.cislovoddilu AND
                iu2.priznakanvedlejsiudalost=false
            )
            WHERE
                iu.priznakanvedlejsiudalost=true AND
                iu2.precteno IS NULL AND
                iu.typudalosti = :typudalosti
        """
        rows = await self.db.fetch_all(query=query, values={"typudalosti": 64})

        while len(self.tasks) < self.config["concurrency"]:
            if not rows:
                break
            self.schedule_task(session, rows.pop(0))

        while len(self.tasks):
            front = self.tasks.pop(0)
            try:
                await front.task
            except (asyncio.TimeoutError, aiohttp.ServerConnectionError) as e:
                front.logger.info(f"Retrying {front.doc_id} due to error: {e.__class__.__name__}: {e}")
                try:
                    self.tasks.insert(0, front.retry())
                except Exception as e:
                    # Cannot retry(), application is expected to exit
                    front.logger.exception("Retry error")
                    print(f"Abort: {e}")
                    await self.cancel_tasks()
                    return
            except:
                front.logger.exception("Import processing error")

            if len(self.tasks) < self.config["concurrency"]:
                if rows:
                    self.schedule_task(session, rows.pop(0))

    async def run(self):
        await self.db.connect()

        timeout = aiohttp.ClientTimeout(total=self.config["request_timeout"])
        async with aiohttp.ClientSession(timeout=timeout, raise_for_status=False) as session:
            await self.fetchRows(session)

        await self.db.disconnect()

class DocumentTask:

    def __init__(self, downloader, sess, row):
        self.parent = downloader
        self.config = self.parent.config
        self.sess = sess
        self.row = row
        self.doc_id = row['dokumenturl']
        self.url = IsirUdalost.DOC_PREFIX + self.doc_id
        self.retry_count = 0
        self.finished = False
        self.pdf_path = self.parent.tmp_path + f"/{self.doc_id}.pdf"
        self.log_file = "{0}/{1}.log".format(self.parent.log_path, self.doc_id)
        
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger('dl.doc.' + str(self.doc_id))
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler(self.log_file)
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.WARNING if not self.config['debug'] else logging.DEBUG)
        self.logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO if not self.config['debug'] else logging.DEBUG)
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)
        self.logger.debug("Log opened")

    def __repr__(self):
        return f"doc_id={self.doc_id}"

    def retry(self):
        max_retry = self.parent.config["retry_times"]
        self.finished = False
        self.retry_count += 1
        if self.retry_count > max_retry:
            raise TooManyRetries(f"Doc id={self.doc_id} failed even after max. amount of retries.")
        self.logger.info(f"Retry {self.retry_count} of {max_retry} for {self}")
        self.task = asyncio.create_task(self.run())
        return self

    def rmEmptyLog(self):
        if os.path.getsize(self.log_file) == 0:
            os.remove(self.log_file)

    async def run(self):
        self.logger.info(f"Requesting {self.url}")

        async with self.sess.get(self.url) as resp:
            if resp.status == 200:
                async with aiofiles.open(self.pdf_path, mode='wb') as f:
                    async for chunk in resp.content.iter_chunked(8000):
                        await f.write(chunk)
        
        self.logger.info(f"Downloaded {self.doc_id}")

        scraper = IsirScraper(self.pdf_path, self.parent.config)
        scraper.logger = self.logger
        documents = await scraper.readDocument(self.pdf_path)

        if documents:
            self.logger.info("Parsed {0}, pocet: {1}".format(self.doc_id, len(documents)))
        else:
            self.logger.info(f"Necitelny dokument {self.doc_id}")

        self.logger.debug(json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False))

        importer = DbImport(self.config, db=self.parent.db)
        importer.isir_id = self.doc_id

        async with self.parent.transaction_lock:
            async with self.parent.db.transaction():
                # Import precteneho dokumentu
                try:
                    for documentObj in documents:
                        await importer.importDocument(documentObj.toDict())
                except:
                    self.logger.exception("Import error")

                    # Ulozeni celeho json dokumentu, u ktereho nastal import error
                    json_doc = json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
                    filename = "{0}/{1}.error.json".format(self.parent.log_path, self.doc_id)
                    async with aiofiles.open(filename, mode='w') as f:
                        await f.write(json_doc)

                    self.finished = True
                    return

                # Ulozit zaznam o precteni teto udalosti
                query = "UPDATE isir_udalost SET precteno=:precteno WHERE id=:id"
                values = {
                    "precteno": datetime.now(),
                    "id": self.row["id"]
                }
                await self.parent.db.execute(query=query, values=values)

        self.finished = True
        self.rmEmptyLog()