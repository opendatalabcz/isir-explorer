import os
import json
import asyncio
import aiohttp
import aiofiles
import logging
from databases import Database
from databases.core import Connection
from datetime import datetime
from .errors import TooManyRetries
from ..webservice.isir_models import IsirUdalost
from ..scraper.isir_scraper import IsirScraper
from ..dbimport.db_import import DbImport
from .stats import DownloadStats


class Downloader:

    NOT_FINISHED = 0
    ALL_COMPLETED = 1
    CHUNK_COMPLETED = 2

    def __init__(self, config):
        self.config = config
        self.db = Database(self.config['db.dsn'], min_size=10, max_size=20)
        self.tasks = []
        self.dl_tasks = {}
        self.forceStop = False
        self.typ_udalosti = []
        self.rows = []
        self.transaction_lock = asyncio.Lock()
        self.stats = DownloadStats()
        self.stats_total = DownloadStats()
        self.lastId = [self.config['dl.start'],
                       self.config['dl.start']]  # hlavni, vedlejsi

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
        asyncio_task = asyncio.create_task(request_task.run())
        request_task.task = asyncio_task
        self.dl_tasks[asyncio_task] = request_task
        self.tasks.append(asyncio_task)

    def cancel_tasks_sync(self):
        for task in self.tasks:
            download_task = self.dl_tasks[task]
            download_task.task.cancel()
        self.tasks = []

    async def cancel_tasks(self):
        for task in self.tasks:
            download_task = self.dl_tasks[task]
            try:
                download_task.task.cancel()
                await download_task.task
            except asyncio.CancelledError:
                print(f"{download_task} zrušen")
            except Exception as e:
                print(f"{download_task} se nepodařilo zrušit: {e}")
        self.tasks = []

    async def fetchRows(self):
        """
        Omezeni dotazu dle id je pouzito proto, ze funkce fetchRows muze byt volana pro
        doplneni seznamu dokumentu pro stazeni i v okamziku, kdy nejake ulohy z predchoziho
        seznamu jiz bezi a jeste se u nich neulozila informace dl_precteno.
        """
        typyudalosti = ",".join(self.typ_udalosti)
        query = f"""
        (SELECT id as uid, false as vedlejsi, * FROM isir_udalost
            WHERE
                id > {self.lastId[0]} AND
                priznakanvedlejsiudalost = false AND
                dl_precteno IS NULL AND
                dokumenturl IS NOT NULL AND
                typudalosti IN ({typyudalosti}) ORDER BY id ASC LIMIT 1000)
        UNION
        (SELECT iu.id AS uid, true as vedlejsi, iu2.* FROM isir_udalost iu
            JOIN isir_udalost iu2
            ON (
                iu.spisovaznacka = iu2.spisovaznacka AND
                iu.oddil = iu2.oddil AND
                iu.cislovoddilu = iu2.cislovoddilu AND
                iu2.priznakanvedlejsiudalost = false
            )
            WHERE
                iu.id > {self.lastId[1]} AND
                iu.priznakanvedlejsiudalost = true AND
                iu2.dl_precteno IS NULL AND
                iu2.dokumenturl IS NOT NULL AND
                iu.typudalosti IN ({typyudalosti}) ORDER BY iu.id ASC LIMIT 1000)
        """  # nosec - vlozeni preddefinovanych konstant

        # Odstranit duplicitni udalosti, ktere odkazuji na stejny dokument
        rows = await self.db.fetch_all(query=query)
        rows = sorted(rows, key=lambda i: i['dokumenturl'])
        self.rows = []
        lastDocument = None
        for row in rows:
            if not row['vedlejsi'] and row['uid'] > self.lastId[0]:
                self.lastId[0] = row['uid']
            elif row['vedlejsi'] and row['uid'] > self.lastId[1]:
                self.lastId[1] = row['uid']

            if lastDocument is None or lastDocument != row['dokumenturl']:
                self.rows.append(row)
            lastDocument = row['dokumenturl']

    async def startDownloads(self, session):
        while True:
            finalizeState = await self.downloadChunk(self.config["dl.delay_after"], session)
            if self.forceStop or finalizeState == self.ALL_COMPLETED:
                break
            if self.config["dl.delay"]:
                print("Čekání {0}s".format(self.config["dl.delay"]))
                await asyncio.sleep(self.config["dl.delay"])
        print(self.stats_total)
        await self.stats.save(self.db)

    async def refillTasks(self, finishedTasks, chunk_size, session):
        # Program ukoncen
        if self.forceStop:
            return self.ALL_COMPLETED

        # Zpracovany vsechny dokumenty z databaze?
        if not self.rows:
            await self.fetchRows()
            if not self.rows:
                return self.ALL_COMPLETED

        # Dosazen limit na pocet stazenych dokumentu?
        if self.config["dl.limit"] and self.stats_total.rows + len(self.tasks) >= self.config["dl.limit"]:
            return self.ALL_COMPLETED

        # Dosazen limit velikosti aktualni skupiny?
        if finishedTasks + len(self.tasks) >= chunk_size:
            return self.CHUNK_COMPLETED

        # Pridat novou ulohu pro stazeni dokumentu
        self.schedule_task(session, self.rows.pop(0))
        return self.NOT_FINISHED

    async def downloadChunk(self, chunk_size, session):
        if not self.rows:
            await self.fetchRows()
        finishedTasks = 0
        finalizeState = self.NOT_FINISHED

        while len(self.tasks) < self.config["dl.concurrency"]:
            if not self.rows:
                break
            self.schedule_task(session, self.rows.pop(0))

        while len(self.tasks):
            finished, pending = await asyncio.wait(self.tasks, return_when=asyncio.FIRST_EXCEPTION)
            self.tasks = list(pending)
            for task in finished:
                dl_task = self.dl_tasks[task]
                del self.dl_tasks[task]
                try:
                    raise task.exception()
                except DownloadTaskFinished:
                    pass
                except (asyncio.TimeoutError, aiohttp.ClientResponseError, aiohttp.ClientConnectionError,
                        aiohttp.ClientPayloadError, aiohttp.http_exceptions.HttpProcessingError) as e:
                    dl_task.logger.info(
                        f"Opakování {dl_task} kvůli chybě: {e.__class__.__name__}: {e}")
                    try:
                        dl_task.retry()
                        self.dl_tasks[dl_task.task] = dl_task
                        self.tasks.append(dl_task.task)
                        continue
                    except Exception as e:
                        dl_task.logger.exception(f"Nelze opakovat: {e}")
                except KeyboardInterrupt:
                    pass
                except:
                    dl_task.logger.exception("Chyba během zpracování importu")

                finishedTasks += 1
                self.stats.add(dl_task)
                self.stats_total.add(dl_task)
                if self.stats.rows >= 1000:
                    await self.stats.save(self.db)
                    self.stats = DownloadStats()

            # Nahradit dokoncenou ulohu novym stahovanim
            while not finalizeState and len(self.tasks) < self.config["dl.concurrency"]:
                finalizeState = await self.refillTasks(finishedTasks, chunk_size, session)

        return finalizeState or self.ALL_COMPLETED

    async def run(self):
        await self.db.connect()

        rows = await self.db.fetch_all(query="SELECT id, nazev FROM isir_cis_udalosti WHERE je_citelna = TRUE")
        for row in rows:
            self.typ_udalosti.append(str(row["id"]))

        timeout = aiohttp.ClientTimeout(
            total=self.config["dl.request_timeout"])
        async with aiohttp.ClientSession(timeout=timeout, raise_for_status=False) as session:
            await self.startDownloads(session)

        await self.db.disconnect()

        if self.forceStop:
            asyncio.get_event_loop().stop()


class DocumentTask:

    def __init__(self, downloader, sess, row):
        self.parent = downloader
        self.config = self.parent.config
        self.sess = sess
        self.row = row
        self.task = None
        self.doc_id = row['dokumenturl']
        self.url = IsirUdalost.DOC_PREFIX + self.doc_id
        self.retry_count = 0
        self.finished = False
        self.success = False
        self.documents = []
        self.file_size = 0
        self.empty_document = False
        self.pdf_path = self.parent.tmp_path + f"/{self.doc_id}.pdf"
        self.log_file = "{0}/{1}.log".format(self.parent.log_path, self.doc_id)

        logFormatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s]  %(message)s")
        self.logger = logging.getLogger('dl.doc.' + str(self.doc_id))
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler(self.log_file)
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(
            logging.WARNING if not self.config['debug'] else logging.DEBUG)
        self.logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(
            logging.INFO if not self.config['debug'] else logging.DEBUG)
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)
        self.logger.debug("Počátek logu")

    def __repr__(self):
        return f"doc_id={self.doc_id}"

    def __del__(self):
        self.cleanup()

    def retry(self):
        max_retry = self.parent.config["dl.retry_times"]
        self.finished = False
        self.retry_count += 1
        if self.retry_count > max_retry:
            raise TooManyRetries(
                f"Dokument id={self.doc_id} se nepodařilo stáhnou po max. počtu opakování.")
        self.logger.info(f"Pokus {self.retry_count} z {max_retry} pro {self}")
        self.task = asyncio.create_task(self.run())
        return self

    def cleanup(self):
        # Uzavrit otevrene log soubory
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

        has_logfile = (os.path.getsize(self.log_file) > 0)
        if not has_logfile:
            os.remove(self.log_file)

        remove_pdf = not self.parent.config["dl.keep_pdf"]
        if "log" == self.parent.config["dl.keep_pdf"]:
            remove_pdf = not has_logfile

        # Odstranit vstupni pdf soubor
        if remove_pdf:
            try:
                os.remove(self.pdf_path)
            except FileNotFoundError:
                # Pokud je aktivni save_unreadable, soubor mohl byt jiz presunut
                pass

    async def markAsRead(self, conn):
        # Ulozit zaznam o precteni tohoto dokumentu (vsechny jeho udalosti)
        query = """UPDATE isir_udalost SET dl_precteno=:dl_precteno
            WHERE
                spisovaznacka=:spisovaznacka AND
                oddil=:oddil AND
                cislovoddilu=:cislovoddilu
        """
        values = {
            "dl_precteno": datetime.now(),
            "spisovaznacka": self.row["spisovaznacka"],
            "oddil": self.row["oddil"],
            "cislovoddilu": self.row["cislovoddilu"],
        }
        async with conn:
            await conn.execute(query=query, values=values)

    async def run(self):
        # Manualni vytvoreni Connection objektu kvuli nedostatku v issue #230 (encode/databases)
        conn = Connection(self.parent.db._backend)
        await self.markAsRead(conn)

        self.logger.info(f"Stahování {self.url}")

        async with self.sess.get(self.url) as resp:
            if resp.status == 200:
                async with aiofiles.open(self.pdf_path, mode='wb') as f:
                    async for chunk, _ in resp.content.iter_chunks():
                        self.file_size += len(chunk)
                        await f.write(chunk)
            elif resp.status == 404:
                raise DocumentRemoved(f"Dokument {self.doc_id} neexistuje")
            else:
                raise aiohttp.http_exceptions.HttpProcessingError(
                    code=resp.status, message=f"HTTP {resp.status}")

        self.logger.info(f"Stažen dokument {self.doc_id}")

        scraper = IsirScraper(self.pdf_path, self.parent.config)
        scraper.logger = self.logger
        self.documents = await scraper.readDocument(self.pdf_path)

        if self.documents:
            self.logger.info("Přečten dokument {0}, dokumentů: {1}".format(
                self.doc_id, len(self.documents)))
        else:
            if scraper.is_empty:
                self.empty_document = True
                self.logger.info(f"Prázdný dokument {self.doc_id}")
            else:
                self.logger.info(f"Nečitelný dokument {self.doc_id}")

        self.logger.debug(json.dumps(self.documents, default=lambda o: o.__dict__,
                                     sort_keys=True, indent=4, ensure_ascii=False))
        async with conn:

            importer = DbImport(self.config, db=self.parent.db)
            importer.metadata = {
                "pdf_file_size": self.file_size / 1048576,   # MiB
                "isir_record": self.row,
                "db_conn": conn,
            }

            async with conn.transaction():
                # Import precteneho dokumentu
                try:
                    for documentObj in self.documents:
                        await importer.importDocument(documentObj.toDict())
                except KeyboardInterrupt:
                    raise
                except:
                    self.logger.exception(
                        f"Chyba importu dokumentu {self.doc_id}")

                    # Ulozeni celeho json dokumentu, u ktereho nastal import error
                    json_doc = json.dumps(
                        self.documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
                    filename = "{0}/{1}.error.json".format(
                        self.parent.log_path, self.doc_id)
                    async with aiofiles.open(filename, mode='w') as f:
                        await f.write(json_doc)

                    self.finished = True
                    raise DownloadTaskFinished()

        self.success = True
        self.finished = True
        raise DownloadTaskFinished()


class DownloadTaskFinished(Exception):
    pass


class DocumentRemoved(Exception):
    pass
