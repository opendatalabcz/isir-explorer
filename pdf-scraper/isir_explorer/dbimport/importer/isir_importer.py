from datetime import datetime

class IsirImporter:

    def __init__(self, db, document):
        self.db = db
        self.db_conn = db
        self.doc = document
        self.isir_id = None
        self.isir_ins = None
        self.pdf_file_size = None
        
        # can be postgresql / postgres
        if "postgres" in self.db.url.scheme:
            self.dbtype = "postgres"
        else:
            self.dbtype = self.db.url.scheme

    async def insert(self, table, data):
        column_names = list(data.keys())
        placeholders = map(lambda x:":"+x, column_names)
        query = f"INSERT INTO {table} (" + ",".join(column_names) + ") VALUES ("+ ",".join(placeholders) +")"

        if "postgres" == self.dbtype:
            query += " RETURNING id"

        rowid = await self.db_conn.execute(query=query, values=data)
        return rowid
    
    async def insertMany(self, table, dataset):
        if not dataset:
            return
        data = dataset[0]
        column_names = list(data.keys())
        placeholders = map(lambda x:":"+x, column_names)
        query = f"INSERT INTO {table} (" + ",".join(column_names) + ") VALUES ("+ ",".join(placeholders) +")"
        await self.db_conn.execute_many(query=query, values=dataset)

    def addIsirRecord(self, record):
        """Asociace importovaneho dokumentu k radku v isir_udalost
        """
        self.isir_id = record['dokumenturl']
        self.isir_ins = record["spisovaznacka"]

    def dateFormat(self, date):
        """ Konverze data do formátu data pro databázi (datetimeobject)
        Vstupní formát je české zadání typu d.m.r

        """
        if date is None:
            return None
        date.replace(' ', '')
        try:
            datetimeobject = datetime.strptime(date, '%d.%m.%Y')
        except:
            return None
        return datetimeobject

    async def startImport(self):
        try:
            verze_dokument = self.doc["Metadata"]["Verze"][:10]
        except (KeyError, TypeError):
            verze_dokument = None

        try:
            verze_scraper = self.doc["Metadata"]["Verze_scraper"]
        except KeyError:
            verze_scraper = 1

        dokumentId = await self.insert("dokument",{
            "isir_id": 
                self.isir_id,
            "spisova_znacka":
                self.isir_ins,
            "typ":
                self.TYP_DOKUMENTU,
            "verze_dokument":
                verze_dokument,
            "verze_scraper":
                verze_scraper,
            "pdf_velikost":
                self.pdf_file_size,
            "datum":
                datetime.now(),
        })

        await self.importDocument(dokumentId)

    async def importDocument(self, dokumentId):
        pass