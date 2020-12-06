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

    def __init__(self, filename, config):
        self.config = config
        self.filename = filename
        self.db = Database(self.config['db.dsn'])

        base = os.path.basename(self.filename)
        parts = os.path.splitext(base)
        self.file_name = parts[0]

    async def importDocument(self, doc):
        try:
            typ = doc["Metadata"]["Typ"]
            importerCls = self.IMPORT_CLASS[typ]
        except KeyError:
            raise UnknownDocument()

        importer = importerCls(self.db, doc)
        await importer.startImport()

    async def run(self):

        with open(self.filename,'r') as f:
            fileContent = f.read()
        obj = json.loads(fileContent)

        # json muze obsahovat jeden nebo vice dokumentu
        documents = []
        if isinstance(obj, list): 
            documents = obj
        else: 
            documents.append(obj)

        await self.db.connect()
        for document in documents:
            await self.importDocument(document)
        await self.db.disconnect()