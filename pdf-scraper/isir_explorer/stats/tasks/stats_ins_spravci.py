from ..task import Task


class StatsInsSpravci(Task):

    def sestavitJmeno(self, osoba):
        
        nazev = osoba["nazevosoby"]
        jmeno = None
        prijmeni = None

        if osoba["jmeno"]:

            nazev = osoba["jmeno"] + " " + osoba["nazevosoby"]

            if osoba["titulpred"]:
                nazev = osoba["titulpred"].strip() + " " + nazev

            if osoba["titulza"]:
                nazev = nazev + " " + osoba["titulza"].strip()

            jmeno = osoba["jmeno"]
            prijmeni = osoba["nazevosoby"]

        return nazev, jmeno, prijmeni

    async def spravciPodnikatele(self):

        rows = await self.db.fetch_all(query="""
                SELECT DISTINCT ic FROM isir_osoba WHERE druhrolevrizeni = '2' AND ic IS NOT NULL
            """)

        for row in rows:
            ic = row["ic"]

            osoba = await self.db.fetch_one(query="""
                SELECT * FROM isir_osoba io
                WHERE
                    druhrolevrizeni = '2' AND
                    ic = :ic AND
                    NOT EXISTS (SELECT id FROM stat_spravce ss WHERE ss.ic = io.ic)
                ORDER BY id DESC LIMIT 1
            """, values={"ic": ic})

            if osoba is None:
                continue

            nazev, jmeno, prijmeni = self.sestavitJmeno(osoba)

            await self.db.execute(query="""INSERT INTO stat_spravce
                (ic, nazev, jmeno, prijmeni)
            VALUES
                (:ic, :nazev, :jmeno, :prijmeni)""", values={
                    "ic": osoba["ic"],
                    "nazev": nazev,
                    "jmeno": jmeno,
                    "prijmeni": prijmeni,
                })

    async def spravciNepodnikatele(self):

        rows = await self.db.fetch_all(query="""
                SELECT nazevosoby, jmeno FROM isir_osoba WHERE druhrolevrizeni = '2' AND ic IS NULL GROUP BY nazevosoby, jmeno
            """)

        for row in rows:
            
            osoba = await self.db.fetch_one(query="""
                SELECT * FROM isir_osoba io
                WHERE
                    druhrolevrizeni = '2' AND
                    nazevosoby = :nazevosoby AND
                    jmeno = :jmeno AND
                    NOT EXISTS (SELECT id FROM stat_spravce ss WHERE
                        ss.ic IS NULL AND
                        ss.prijmeni = io.nazevosoby AND
                        ss.jmeno = io.jmeno)
                ORDER BY id DESC LIMIT 1
            """, values={"nazevosoby": row["nazevosoby"], "jmeno": row["jmeno"]})

            if osoba is None:
                continue

            nazev, jmeno, prijmeni = self.sestavitJmeno(osoba)

            await self.db.execute(query="""INSERT INTO stat_spravce
                (ic, nazev, jmeno, prijmeni)
            VALUES
                (:ic, :nazev, :jmeno, :prijmeni)""", values={
                    "ic": None,
                    "nazev": nazev,
                    "jmeno": jmeno,
                    "prijmeni": prijmeni,
                })

    async def run(self):

        await self.spravciPodnikatele()
        await self.spravciNepodnikatele()

