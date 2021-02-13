import os
import json
from databases import Database
from .errors import UnknownDocument
from .importer.prihlaska_pohledavky import PrihlaskaImporter
from .importer.prehledovy_list import PrehledovyListImporter
from .importer.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeniImporter
from .importer.zprava_pro_oddluzeni import ZpravaProOddluzeniImporter
from .importer.zprava_splneni_oddluzeni import ZpravaSplneniOddluzeniImporter


class DbImport:

    IMPORT_CLASS = {
        "PrihlaskaPohledavky": PrihlaskaImporter,
        "PrehledovyList": PrehledovyListImporter,
        "ZpravaProOddluzeni": ZpravaProOddluzeniImporter,
        "ZpravaPlneniOddluzeni": ZpravaPlneniOddluzeniImporter,
        "ZpravaSplneniOddluzeni": ZpravaSplneniOddluzeniImporter,
    }

    def __init__(self, config, db=None):
        self.config = config
        if db is None:
            self.db = Database(self.config['db.dsn'])
        else:
            self.db = db
        self.metadata = {}

    async def importDocument(self, doc):
        try:
            typ = doc["Metadata"]["Typ"]
            importerCls = self.IMPORT_CLASS[typ]
        except KeyError:
            raise UnknownDocument()

        importer = importerCls(self.db, doc)

        if "isir_record" in self.metadata:
            importer.addIsirRecord(self.metadata["isir_record"])

        if "pdf_file_size" in self.metadata:
            importer.pdf_file_size = round(self.metadata["pdf_file_size"], 3)

        if "db_conn" in self.metadata:
            importer.db_conn = self.metadata["db_conn"]

        await importer.startImport()

    async def run(self, filename):

        with open(filename, 'r') as f:
            fileContent = f.read()
        obj = json.loads(fileContent)

        # json muze obsahovat jeden nebo vice dokumentu
        documents = []
        if isinstance(obj, list):
            documents = obj
        else:
            documents.append(obj)

        await self.db.connect()

        async with self.db.transaction():
            for document in documents:
                await self.importDocument(document)

        await self.db.disconnect()
