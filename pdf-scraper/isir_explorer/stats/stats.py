import os
import json
from databases import Database
import importlib

class IsirStats:

    TASKS_PACKAGE = 'isir_explorer.stats.tasks'

    def __init__(self, config, db=None):
        self.config = config
        if db is None:
            self.db = Database(self.config['db.dsn'])
        else:
            self.db = db

    def prevodNaClassName(self, name):
        tmp = name.replace("_", " ").replace(".","")
        return ''.join(x for x in tmp.title() if not x.isspace())

    async def run(self, name):
        clsName = self.prevodNaClassName(name)

        import_name = "." + name
        try:
            taskCls = getattr(importlib.import_module(import_name, package=self.TASKS_PACKAGE), clsName)
        except ModuleNotFoundError:
            print(f"Uloha s nazvem \"{name}\" neexistuje!")
            exit(1)

        task = taskCls(self.config, db=self.db)

        await self.db.connect()
        
        await task.run()

        await self.db.disconnect()