import aiohttp
import xml.etree.ElementTree as ET
from .exceptions import IsirServiceException, TooManyRetries, NoRecordsInResponse
from .isir_models import IsirOsoba, IsirUdalost, IsirVec, IsirStavVeci, IsirAdresa
import asyncio
import time
import concurrent.futures
import re


class IsirRequests:

    SPEED_SAMPLES = 5

    def __init__(self, conf, db):
        self.conf = conf
        self.db = db
        self.front_task_done = asyncio.Event()
        self.last_completed_id = None
        self.tasks = []
        self.pos = 0
        self.exit_code = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.conf["concurrency"],
        )
        self.speedCounter = {"samples": 0}
        self.ins_filter = re.compile(
            self.conf["ins_filter"]) if self.conf["ins_filter"] is not None else None

        # can be postgresql / postgres
        if "postgres" in self.db.url.scheme:
            self.dialect = "postgres"
        else:
            self.dialect = self.db.url.scheme

    def schedule_task(self, session, pos):
        if self.conf["max_id"] is not None and self.pos > self.conf["max_id"]:
            return

        request_task = RequestTask(self, session, pos)
        request_task.task = asyncio.create_task(request_task.run())
        self.pos += 1000
        self.tasks.append(request_task)

    async def cancel_tasks(self):
        for download_task in self.tasks:
            try:
                download_task.task.cancel()
                await download_task.task
            except asyncio.CancelledError:
                self.log(f"{download_task} zrusen", 10)
            except NoRecordsInResponse:
                self.log(
                    f"{download_task} vratil prazdny vysledek jeste pred zrusenim", 10)
            except Exception as e:
                self.log(f"{download_task} se nepodaril zrusit: {e}", 10)
        try:
            await self.db.close()
        except:
            self.log("Nepodarilo se uzavrit db spojeni!", 10)
        self.tasks = []

    async def start(self):
        timeout = aiohttp.ClientTimeout(total=self.conf["request_timeout"])
        headers = {'Accept': 'text/xml',
                   'Content-Type': 'text/xml;charset=UTF-8'}

        self.last_completed_id = self.pos = await self.get_last_id()
        self.front_task_done.clear()
        async with aiohttp.ClientSession(timeout=timeout, headers=headers, raise_for_status=False) as session:
            await self.requests_loop(session)

    async def requests_loop(self, session):
        for i in range(self.conf["concurrency"]):
            self.schedule_task(session, self.pos)

        while len(self.tasks):
            front = self.tasks.pop(0)
            try:
                await front.task
            except NoRecordsInResponse:
                self.log(f"{front} returned empty result", 5)
                self.log(
                    "Dokonceno - ISIR databaze synchronizovana a je aktualni!")
                await self.cancel_tasks()
                return
            except (asyncio.TimeoutError, IsirServiceException, aiohttp.ServerConnectionError) as e:
                self.log(
                    f"Opakovani {front} kvuli chybe: {e.__class__.__name__}: {e}")
                try:
                    self.tasks.insert(0, front.retry())
                except Exception as e:
                    # Cannot retry(), application is expected to exit
                    await self.cancel_tasks()
                    self.log(f"Abort: {e}")
                    self.exit_code = 10
                    return

            if front.finished:
                self.last_completed_id = front.pos + 1000
                self.front_task_done.set()

            if len(self.tasks) < self.conf["concurrency"]:
                self.schedule_task(session, self.pos)

    async def get_last_id(self):
        if self.conf["last_id"] is not None:
            return self.conf["last_id"]

        row = await self.db.fetch_one(query=f"SELECT MAX(id) FROM {IsirUdalost.TABLE_NAME}")
        last_id = row[0]

        if last_id is None:
            last_id = 0

        if self.conf["min_id"] is not None and last_id < self.conf["min_id"]:
            last_id = self.conf["min_id"]

        return last_id

    def log(self, msg, level=1):
        if self.conf["silent"]:
            return

        if level >= 5 and not self.conf["verbose"]:
            return

        print(msg)

    def showSpeed(self, cnt):
        if self.speedCounter["samples"] == 0:
            self.speedCounter["ts"] = time.time()
            self.speedCounter["cnt"] = 0
        self.speedCounter["samples"] += 1
        self.speedCounter["cnt"] += cnt

        if self.speedCounter["samples"] == self.SPEED_SAMPLES:
            self.speedCounter["samples"] = 0
            end = time.time()
            diff = end - self.speedCounter["ts"]
            per_request = diff / self.SPEED_SAMPLES
            per_record = (diff / self.speedCounter["cnt"]) * 1000
            print(
                f"TIME per request = {per_request} sec, record = {per_record} ms")


class RequestTask:
    """ Wrapper around asyncio task with information about the download job"""

    ISIR_SERVICE = 'https://isir.justice.cz:8443/isir_public_ws/IsirWsPublicService'

    NAMESPACES = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'isir': 'http://isirpublicws.cca.cz/types/'
    }

    NOT_STORED_UDALOST_TYPES = [1, 2, 4, 330, 405, 371]

    def __init__(self, requests_instance, session, pos):
        self.parent = requests_instance
        self.db = requests_instance.db
        self.session = session
        self.pos = pos
        self.retry_count = 0
        self.task = None
        self.finished = False
        self.log = self.parent.log

    @staticmethod
    def get_isir_documnet_url(aid):
        return f"https://isir.justice.cz:8443/isir_public_ws/doc/Document?idDokument={aid}"

    @staticmethod
    def get_isir_request_body(aid):
        return ('<soapenv:Envelope '
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:typ="http://isirpublicws.cca.cz/types/">'
                '<soapenv:Header/>'
                '<soapenv:Body>'
                '<typ:getIsirWsPublicIdDataRequest>'
                '<idPodnetu>' + str(aid) + '</idPodnetu>'
                '</typ:getIsirWsPublicIdDataRequest>'
                '</soapenv:Body>'
                '</soapenv:Envelope>')

    def retry(self):
        max_retry = self.parent.conf["retry_times"]
        self.finished = False
        self.retry_count += 1
        if self.retry_count > max_retry:
            raise TooManyRetries(
                f"Task pos={self.pos} failed even after max. amount of retries.")
        self.log(f"Retry {self.retry_count} of {max_retry} for {self}")
        self.task = asyncio.create_task(self.run())
        return self

    def __repr__(self):
        return f"Task pos={self.pos}"

    async def run(self):
        body = self.get_isir_request_body(self.pos)
        async with self.session.post(self.ISIR_SERVICE, data=body) as resp:
            if resp.status != 200:
                raise IsirServiceException(
                    f"Isir service returned HTTP {resp.status}")
            data = await resp.text('utf-8')
            await self.process_response(data)

    async def process_response(self, data):
        root = ET.fromstring(data)
        body = root.find('soap:Body', self.NAMESPACES)
        isir_res = body.find(
            'isir:getIsirWsPublicDataResponse', self.NAMESPACES)
        status = isir_res.find('status')
        stav = status.find('stav').text
        if stav != "OK":
            msg = status.find('kodChyby').text + ' - ' + \
                status.find('popisChyby').text
            raise IsirServiceException(msg)

        records = isir_res.findall('data')

        if len(records) == 0:
            raise NoRecordsInResponse("Result set empty.")

        await self.save_records(records)

    async def model_change(self, model):
        await self.db.execute(query=model.get_insert_query(self.parent.dialect), values=model.get_db_data())

    def parseRows(self, records):
        udalost_rows = []
        models = []
        for r in records:
            u = IsirUdalost(r)

            if self.parent.ins_filter is not None:
                if not self.parent.ins_filter.match(u.spisovaZnacka):
                    continue

            if u.typUdalosti not in self.NOT_STORED_UDALOST_TYPES:
                if u.oddil is None or u.cisloVOddilu is None:
                    pass
                else:
                    udalost_rows.append(u)

            xml_elem = u.poznamka.find("osoba")
            if xml_elem is not None:
                osoba = IsirOsoba(xml_elem, u)
                osoba.soud = u.data["soud"]
                osoba.datumZalozeni = u.data["datumZalozeniUdalosti"]
                osoba.idZalozeni = u.data["id"]
                models.append(osoba)

                # Pokud je u osoby evidovana i adresa
                xml_elem = xml_elem.find("adresa")
                if xml_elem is not None:
                    adresa = IsirAdresa(xml_elem, u)
                    adresa.idOsoby = osoba.idOsoby
                    models.append(adresa)

            xml_elem = u.poznamka.find("vec")
            if xml_elem is not None:
                models.append(IsirVec(xml_elem, u))
                models.append(IsirStavVeci(xml_elem, u))

        return udalost_rows, models

    async def save_records(self, records):
        if self.parent.conf["parse_in_executor"]:
            loop = asyncio.get_event_loop()
            blocking_task = loop.run_in_executor(
                self.parent.executor, self.parseRows, records)
            completed, pending = await asyncio.wait([blocking_task])
            for e in completed:
                break
            udalost_rows, models = e.result()
        else:
            udalost_rows, models = self.parseRows(records)

        # Model updated must be done sequentially, wait until the current request is first in line
        while True:
            if self.parent.last_completed_id == self.pos:
                break
            await self.parent.front_task_done.wait()
            self.parent.front_task_done.clear()

        async with self.db.transaction():
            for u in udalost_rows:
                await self.db.execute(query=u.get_insert_query(self.parent.dialect), values=u.get_db_data())

        # Make all updates in 1 transaction (application can be stopped during iteration)
        async with self.db.transaction():
            for m in models:
                await self.model_change(m)

        self.log(f"{self} Completed")
        self.parent.showSpeed(len(records))
        self.finished = True
