from ..task import Task


class DoplnitDatumZverejneniDokument(Task):

    async def run(self):
        print("Hledani asociace ...")
        rows = await self.db.fetch_all(query="""
                SELECT id, isir_id FROM dokument WHERE zverejneni IS NULL
            """)
        print("Probiha spojovani ...")
        i = 0
        for row in rows:
            i += 1
            isir_id = row["isir_id"]
            udalost = await self.db.fetch_one(query="""
                SELECT datumzverejneniudalosti FROM isir_udalost WHERE dokumenturl=:isir_id
            """, values={
                "isir_id": isir_id,
            })

            if udalost is None:
                continue

            await self.db.execute(query="""
                UPDATE dokument SET zverejneni=:zverejneni WHERE id=:id
            """, values={
                "id": row["id"],
                "zverejneni": udalost["datumzverejneniudalosti"],
            })

            if i % 1000 == 0:
                print("Zpracovano {0} ...".format(i))
