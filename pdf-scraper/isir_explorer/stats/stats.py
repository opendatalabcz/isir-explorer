import os
import json
from databases import Database
from .tasks.link_prihlaska_osoba import LinkPrihlaskaOsoba
from .tasks.doplnit_cislo_prihlasky import DoplnitCisloPrihlasky
from .tasks.odstranit_duplicitni_zmeny_stavu import OdstranitDuplicitniZmenyStavu

class IsirStats:

    def __init__(self, config, db=None):
        self.config = config
        if db is None:
            self.db = Database(self.config['db.dsn'])
        else:
            self.db = db

    async def run(self, name):
        await self.db.connect()

        #task = LinkPrihlaskaOsoba(self.config, self.db)
        #task = DoplnitCisloPrihlasky(self.config, self.db)
        task = OdstranitDuplicitniZmenyStavu(self.config, self.db)
        
        await task.run()

        await self.db.disconnect()