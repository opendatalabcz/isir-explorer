from ..task import Task


class DoplnitCisloVeritele(Task):

    async def run(self):
        print("Hledani asociace ...")
        # pl_id, cislo_veritele, spis, isir_osoba_veritel
        rows = await self.db.fetch_all(query="""
                SELECT pl_id,cislo_veritele, spis, isir_osoba_veritel FROM (
                    SELECT pl_id, cislo_veritele, d.spisova_znacka spis, (
                        SELECT isir_osoba
                        FROM pp_osoba
                        JOIN dokument ON (pp_osoba.pp_id = dokument.id)
                        JOIN prihlaska_pohledavky pp ON (pp.id = dokument.id)
                        WHERE
                            dokument.spisova_znacka = d.spisova_znacka AND
                            pp.cislo_prihlasky = pl_pohledavka.cislo_prihlasky
                        LIMIT 1
                    ) isir_osoba_veritel
                    FROM pl_pohledavka
                    LEFT JOIN dokument d ON (pl_pohledavka.pl_id = d.id)
                    WHERE pl_pohledavka.osoba_spojena IS NULL
                ) a
                WHERE a.isir_osoba_veritel IS NOT NULL
                GROUP BY pl_id, cislo_veritele, spis, isir_osoba_veritel
            """)
        print("Probiha spojovani ...")
        i = 0
        for row in rows:
            i += 1
            await self.db.execute(query="""
                UPDATE pl_pohledavka SET veritel_id=:veritel_id, osoba_spojena=1
                WHERE pl_id=:pl_id AND cislo_veritele=:cislo_veritele
            """, values={
                "veritel_id": row["isir_osoba_veritel"],
                "pl_id": row["pl_id"],
                "cislo_veritele": row["cislo_veritele"],
            })

            await self.db.execute(query="""
                UPDATE isir_osoba SET cislo_veritele=:cislo_veritele WHERE id=:veritel_id
            """, values={
                "veritel_id": row["isir_osoba_veritel"],
                "cislo_veritele": row["cislo_veritele"],
            })

            if i % 1000 == 0:
                print("Zpracovano {0} ...".format(i))
