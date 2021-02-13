from ..task import Task


class DoplnitDatumZahajeni(Task):

    async def run(self):
        print("Hledani asociace ...")
        rows = await self.db.fetch_all(query="""
                SELECT spisovaznacka FROM isir_vec WHERE datumzahajeni IS NULL
            """)
        print("Probiha spojovani ...")
        i = 0
        for row in rows:
            i += 1
            vec = row["spisovaznacka"]
            row = await self.db.fetch_one(query="""
                SELECT MIN(datumzalozeniudalosti) AS datumzalozeniudalosti FROM isir_udalost WHERE spisovaznacka=:vec
            """, values={
                "vec": vec,
            })

            await self.db.execute(query="""
                UPDATE isir_vec SET datumzahajeni=:datumzahajeni WHERE spisovaznacka=:vec
            """, values={
                "vec": vec,
                "datumzahajeni": row["datumzalozeniudalosti"],
            })

            if i % 1000 == 0:
                print("Zpracovano {0} ...".format(i))
