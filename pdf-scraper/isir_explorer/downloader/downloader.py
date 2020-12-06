import os
import json
import asyncio
import aiohttp
import aiofiles
import logging
from databases import Database
from .errors import DownloaderException, TooManyRetries
from ..webservice.isir_models import IsirUdalost
from ..scraper.isir_scraper import IsirScraper

class Downloader:

    def __init__(self, config):
        self.config = config
        self.db = Database(self.config['db.dsn'])
        self.tasks = []

        self.tmp_base = self.config['tmp_dir'].rstrip("/")
        self.tmp_path = self.tmp_base + "/pdf"
        self.log_path = self.tmp_base + "/log"
        self.tmpDir()

    def tmpDir(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    async def fetchRows(self, session):
        query = "SELECT * FROM isir_udalost WHERE typudalosti = :typudalosti ORDER BY id ASC LIMIT 10"
        rows = await self.db.fetch_all(query=query, values={"typudalosti": 63})
        
        for row in rows:
            request_task = DocumentTask(self, session, row)
            request_task.task = asyncio.create_task(request_task.run())
            self.tasks.append(request_task)

        while len(self.tasks):
            front = self.tasks.pop(0)
            try:
                await front.task
            except (asyncio.TimeoutError, aiohttp.ServerConnectionError) as e:
                self.log(f"Retrying {front} due to error: {e.__class__.__name__}: {e}")
                try:
                    pass
                    self.tasks.insert(0, front.retry())
                except Exception as e:
                    # Cannot retry(), application is expected to exit
                    await self.cancel_tasks()
                    self.log(f"Abort: {e}")
                    self.exit_code = 10
                    return

            #if len(self.tasks) < self.conf["concurrency"]:
            #    self.schedule_task(session, self.pos)

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
        
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger('dl.doc.' + str(self.doc_id))
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler("{0}/{1}.log".format(self.parent.log_path, self.doc_id))
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.ERROR if not self.config['debug'] else logging.DEBUG)
        self.logger.addHandler(fileHandler)

        if self.config['debug']:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(logging.INFO)
            consoleHandler.setFormatter(logFormatter)
            self.logger.addHandler(consoleHandler)
        self.logger.debug("Log opened")

    def retry(self):
        max_retry = self.parent.config["retry_times"]
        self.finished = False
        self.retry_count += 1
        if self.retry_count > max_retry:
            raise TooManyRetries(f"Doc id={self.doc_id} failed even after max. amount of retries.")
        self.log(f"Retry {self.retry_count} of {max_retry} for {self}")
        self.task = asyncio.create_task(self.run())
        return self

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

        self.logger.info(f"Parsed {self.doc_id}")

        self.logger.debug(json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False))

        self.finished = True