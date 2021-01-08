import os
import json
from databases import Database
from .tasks.link_prihlaska_osoba import LinkPrihlaskaOsoba

class IsirStats:

    def __init__(self, config, db=None):
        self.config = config
        if db is None:
            self.db = Database(self.config['db.dsn'])
        else:
            self.db = db

    async def run(self, name):
        await self.db.connect()
        print("OK")

        task = LinkPrihlaskaOsoba(self.config, self.db)
        await task.run()

        await self.db.disconnect()