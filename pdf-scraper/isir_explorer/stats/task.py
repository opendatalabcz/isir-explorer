from databases import Database


class Task:

    def __init__(self, config, db=None):
        self.config = config
        if db is None:
            self.db = Database(self.config['db.dsn'])
        else:
            self.db = db

    async def run(self):
        pass
