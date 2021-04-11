from ..task import Task


class OdstranitDuplicitniZmenyStavu(Task):
    """2019: 1710718 radku -> 64463 -> 96.2% zaznamu bylo redundantnich
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.duplicit = 0

    async def run(self):
        rows = await self.db.fetch_all(query="""
                SELECT spisovaznacka FROM isir_vec
            """)
        i = 0
        for row in rows:

            spis = row["spisovaznacka"]

            stavy = await self.db.fetch_all(query="""
                SELECT * FROM isir_vec_stav WHERE spisovaznacka = :spis ORDER BY id ASC
            """, values={
                "spis": spis
            })

            posledni = None
            duplicitni = []
            for stav in stavy:
                if posledni == stav["druhstavrizeni"]:
                    duplicitni.append(str(stav["id"]))
                    self.duplicit += 1
                posledni = stav["druhstavrizeni"]

            if duplicitni:
                query = "DELETE FROM isir_vec_stav WHERE id IN (" + ",".join(duplicitni) + ")" # nosec - bezp. vstup
                await self.db.execute(query=query)
            i += 1

            if i % 100 == 0:
                print("Zpracovano {0} ...".format(i))
        print(f"Odstraneno duplicit: {self.duplicit}")
