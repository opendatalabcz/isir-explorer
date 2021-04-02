from ..task import Task
from isir_explorer.webservice.enums import DRUH_SPRAVCE


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

            await self.db.execute(
                query="""INSERT INTO stat_spravce
                (ic, nazev, jmeno, prijmeni)
            VALUES
                (:ic, :nazev, :jmeno, :prijmeni)""",
                values={
                    "ic": osoba["ic"],
                    "nazev": nazev,
                    "jmeno": jmeno,
                    "prijmeni": prijmeni,
                }
            )

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

            await self.db.execute(
                query="""INSERT INTO stat_spravce
                (ic, nazev, jmeno, prijmeni)
            VALUES
                (:ic, :nazev, :jmeno, :prijmeni)""",
                values={
                    "ic": None,
                    "nazev": nazev,
                    "jmeno": jmeno,
                    "prijmeni": prijmeni,
                }
            )

    async def naleztSpravce(self, isir_osoba):
        if isir_osoba["ic"]:
            return await self.db.fetch_one(query="""
                SELECT id FROM stat_spravce WHERE ic = :ic LIMIT 1
                """, values={"ic": isir_osoba["ic"]}
            )
        else:
            return await self.db.fetch_one(query="""
                SELECT id FROM stat_spravce WHERE jmeno = :jmeno AND prijmeni = :prijmeni LIMIT 1
                """, values={"jmeno": isir_osoba["jmeno"], "prijmeni": isir_osoba["nazevosoby"]}
            )

    async def priraditSpravceIns(self):

        # Vybrat rizeni, ktere dosud nemaji prirazeneho spravce
        rows = await self.db.fetch_all(query="""
                SELECT sv.id, sv.spisovaznacka FROM stat_vec sv
                LEFT JOIN stat_spravce_ins ssi ON (ssi.id_ins = sv.id)
                WHERE ssi.id_spravce IS NULL
            """)

        for row in rows:
            # Najit spravce k danemu INS v isir_osoba
            # Aby bylo mozne evidovat spravce i u starsich rizeni, neni vyuzita podminka
            # datumosobavevecizrusena IS NULL
            spravci = await self.db.fetch_all(query="""
                SELECT * FROM isir_osoba
                WHERE
                    druhrolevrizeni = '2' AND
                    spisovaznacka = :spisovaznacka
            """, values={"spisovaznacka": row["spisovaznacka"]})

            for isir_osoba_spravce in spravci:
                druh = isir_osoba_spravce["druhspravce"]
                
                # Oprava konstant
                if druh == DRUH_SPRAVCE["SPRÁVCE"]:
                    druh = DRUH_SPRAVCE["INS SPRÁV"]
                elif druh == DRUH_SPRAVCE["ZÁST SPR"]:
                    druh = DRUH_SPRAVCE["ZÁST INS S"]
                if not druh:
                    druh = DRUH_SPRAVCE["INS SPRÁV"]

                # Nalezt zaznam konkretniho spravce dle IC nebo jmena
                nalezenySpravce = await self.naleztSpravce(isir_osoba_spravce)

                if not nalezenySpravce:
                    print("{0}: Nelze najit spravce".format(row["spisovaznacka"]))
                    continue

                await self.db.execute(
                    query="""INSERT INTO stat_spravce_ins
                    (id_ins, id_spravce, druh_spravce)
                VALUES
                    (:id_ins, :id_spravce, :druh_spravce)""",
                    values={
                        "id_ins": row["id"],
                        "id_spravce": nalezenySpravce["id"],
                        "druh_spravce": druh,
                    }
                )

    async def run(self):

        await self.spravciPodnikatele()
        await self.spravciNepodnikatele()

        await self.priraditSpravceIns()