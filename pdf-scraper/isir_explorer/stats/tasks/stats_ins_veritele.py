from ..task import Task
from isir_explorer.webservice.enums import DRUH_SPRAVCE
from asyncpg.exceptions import NotNullViolationError

class StatsInsVeritele(Task):


    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.counter = 0

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

    async def veriteleStatistikyRizeni(self):
        self.counter = 0
        rows = await self.db.fetch_all(query="""
                SELECT id, ic FROM stat_veritel WHERE ins_celkem IS NULL
            """)

        for row in rows:
            self.counter += 1
            stats_rizeni = await self.db.fetch_one(query="""
                SELECT COUNT(*) as pocet_rizeni FROM stat_veritel_ins svi
                JOIN stat_vec sv ON (svi.id_ins = sv.id)
                WHERE
                    svi.id_veritel = :id
            """, values={"id": row["id"]})

            stats_pohledavky = await self.db.fetch_one(query="""
                SELECT
                    COUNT(*) AS pocet_prihlasek,
                    SUM(pocet_pohledavek) AS pocet_pohledavek,
                    SUM(celkova_vyse) AS celkova_vyse,
                    SUM(celkova_vyse_nezajistenych) AS celkova_vyse_nezajistenych,
                    SUM(celkova_vyse_zajistenych) AS celkova_vyse_zajistenych
                FROM isir_osoba
                JOIN pp_osoba ON (pp_osoba.isir_osoba = isir_osoba.id)
                JOIN prihlaska_pohledavky pp ON (pp.id = pp_osoba.pp_id)
                WHERE
                    isir_osoba.ic = :ic AND
                    isir_osoba.druhrolevrizeni = '3' AND
                    isir_osoba.datumosobavevecizrusena IS NULL
            """, values={"ic": row["ic"]})

            await self.db.execute(
                query="""UPDATE stat_veritel
                SET 
                    ins_celkem=:ins_celkem,
                    pohledavky_pocet=:pohledavky_pocet,
                    prihlasky_pocet=:prihlasky_pocet,
                    vyse_celkem=:vyse_celkem,
                    vyse_nezaj=:vyse_nezaj,
                    vyse_zaj=:vyse_zaj
                WHERE id=:id
                """,
                values={
                    "id": row["id"],
                    "ins_celkem": stats_rizeni["pocet_rizeni"],
                    "pohledavky_pocet": stats_pohledavky["pocet_pohledavek"],
                    "prihlasky_pocet": stats_pohledavky["pocet_prihlasek"],
                    "vyse_celkem": stats_pohledavky["celkova_vyse"],
                    "vyse_nezaj": stats_pohledavky["celkova_vyse_nezajistenych"],
                    "vyse_zaj": stats_pohledavky["celkova_vyse_zajistenych"],
                }
            )

            if self.counter % 1000 == 0:
                print("Statistiky {0} ...".format(self.counter))

    async def veritelePodnikatele(self):

        rows = await self.db.fetch_all(query="""
                SELECT DISTINCT ic FROM isir_osoba WHERE druhrolevrizeni = '3'
                AND ic IS NOT NULL
                AND datumosobavevecizrusena IS NULL
            """)

        for row in rows:
            self.counter += 1
            ic = row["ic"]

            osoba = await self.db.fetch_one(query="""
                SELECT * FROM isir_osoba io
                WHERE
                    druhrolevrizeni = '3' AND
                    ic = :ic AND
                    datumosobavevecizrusena IS NULL AND
                    NOT EXISTS (SELECT id FROM stat_veritel sv WHERE sv.ic = io.ic)
                ORDER BY id DESC LIMIT 1
            """, values={"ic": ic})

            if osoba is None:
                continue

            nazev, jmeno, prijmeni = self.sestavitJmeno(osoba)

            rowid = await self.db.execute(
                query="""INSERT INTO stat_veritel
                (ic, nazev, jmeno, prijmeni)
            VALUES
                (:ic, :nazev, :jmeno, :prijmeni) RETURNING id""",
                values={
                    "ic": osoba["ic"],
                    "nazev": nazev,
                    "jmeno": jmeno,
                    "prijmeni": prijmeni,
                }
            )
            await self.vlozitRizeniVeritele(osoba["ic"], rowid)

            if self.counter % 1000 == 0:
                print("Zpracovano {0} ...".format(self.counter))

    async def vlozitRizeniVeritele(self, ic, rowid):

        rows = await self.db.fetch_all(query="""
            SELECT DISTINCT spisovaznacka FROM isir_osoba WHERE druhrolevrizeni = '3'
            AND ic = :ic
            AND datumosobavevecizrusena IS NULL
        """, values={
            "ic": ic
        })

        for row in rows:
            spisovaznacka = row['spisovaznacka']
            try:
                await self.db.execute(
                    query="""INSERT INTO stat_veritel_ins
                    (id_ins, id_veritel)
                VALUES
                    ((SELECT id FROM stat_vec WHERE spisovaznacka = :spisovaznacka), :id_veritel)""",
                    values={
                        "spisovaznacka": spisovaznacka,
                        "id_veritel": rowid,
                    }
                )
            except NotNullViolationError:
                pass
        
    async def run(self):

        #await self.veritelePodnikatele()

        await self.veriteleStatistikyRizeni()
