import os
import json
import asyncio
import aiohttp
import aiofiles
from databases import Database
from .errors import DownloaderException, TooManyRetries
from ..webservice.isir_models import IsirUdalost

class Downloader:

    def __init__(self, config):
        self.config = config
        self.db = Database(self.config['db.dsn'])
        self.tasks = []

        self.tmp_path = self.config['tmp_dir'].rstrip("/") + "/pdf"
        self.tmpDir()

    def tmpDir(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

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
        self.sess = sess
        self.row = row
        self.doc_id = row['dokumenturl']
        self.url = IsirUdalost.DOC_PREFIX + self.doc_id
        self.retry_count = 0
        self.finished = False

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
        async with self.sess.get(self.url) as resp:
            if resp.status == 200:
                async with aiofiles.open(self.parent.tmp_dir + f"{self.doc_id}.pdf", mode='wb') as f:
                    async for chunk in resp.content.iter_chunked(8000):
                        await f.write(chunk)
        print(f"Finished {self.doc_id}")
        self.finished = True