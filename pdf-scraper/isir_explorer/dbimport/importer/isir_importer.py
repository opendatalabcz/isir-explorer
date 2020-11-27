class IsirImporter:

    def __init__(self, db, document):
        self.db = db
        self.doc = document
        
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

        rowid = await self.db.execute(query=query, values=data)
        return rowid
    
    async def importDocument(self):
        pass