from ..task import Task


class StatsOddluzeni(Task):

    DOPORUCENI_OSVOBOZENI = "přiznání osvobození od placení zbývajících pohledávek"
    DOPORUCENI_ZRUSENI = "zrušení schváleného oddlužení"

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.posledni_spisovaznacka = ""

    async def seznamInsRizeni(self):
        rows = await self.db.fetch_all(query="""
            SELECT iv.* FROM isir_vec iv
                LEFT JOIN stat_oddluzeni so ON (iv.spisovaznacka = so.spisovaznacka)
            WHERE
                so.id IS NULL AND
                NOT iv.vyrazeno AND
                iv.spisovaznacka > :posledni_spisovaznacka
            ORDER BY iv.spisovaznacka ASC
            LIMIT 5000
        """, values={
            "posledni_spisovaznacka": self.posledni_spisovaznacka
        })
        if rows:
            self.posledni_spisovaznacka = rows[-1]["spisovaznacka"]
        return rows

    def osvobozeni(self, mira, vyse):
        if mira is None or vyse is None or mira == 0:
            return None
        if mira == 100:
            return 0
        celkovy_dluh = vyse/mira * 100
        return celkovy_dluh - vyse

    async def analyzaPohledavekRizeni(self, ins_vec):
        vysledek_oddluzeni = None
        n_osvobozeno = None
        z_osvobozeno = None

        zprava_pro_oddluzeni = await self.db.fetch_one(query="""
            SELECT
            dokument.id AS doc_id
            FROM dokument
            INNER JOIN zprava_pro_oddluzeni zpro ON (zpro.id = dokument.id)
            LEFT JOIN isir_udalost iu ON (iu.dokumenturl = dokument.isir_id)
            WHERE typ = 3 AND spisova_znacka = :spisovaznacka
            ORDER BY iu.datumzalozeniudalosti DESC LIMIT 1
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})

        zprava_splneni_oddluzeni = await self.db.fetch_one(query="""
            SELECT
            dokument.id AS doc_id, zpro.*
            FROM dokument
            INNER JOIN zprava_splneni_oddluzeni zpro ON (zpro.id = dokument.id)
            LEFT JOIN isir_udalost iu ON (iu.dokumenturl = dokument.isir_id)
            WHERE typ = 5 AND spisova_znacka = :spisovaznacka
            ORDER BY iu.datumzalozeniudalosti DESC LIMIT 1
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})

        # Preskocit zapis pokud nejsou evidovana zadna data
        if zprava_pro_oddluzeni is None and zprava_splneni_oddluzeni is None:
            return

        if zprava_splneni_oddluzeni is not None:
            if zprava_splneni_oddluzeni["doporuceni_spravce"] == self.DOPORUCENI_OSVOBOZENI:
                vysledek_oddluzeni = True
            elif zprava_splneni_oddluzeni["doporuceni_spravce"] == self.DOPORUCENI_ZRUSENI:
                vysledek_oddluzeni = False

            if vysledek_oddluzeni:
                n_osvobozeno = self.osvobozeni(
                    zprava_splneni_oddluzeni["n_uspokojeni_mira"], zprava_splneni_oddluzeni["n_uspokojeni_vyse"])
                z_osvobozeno = self.osvobozeni(
                    zprava_splneni_oddluzeni["z_uspokojeni_mira"], zprava_splneni_oddluzeni["z_uspokojeni_vyse"])

        await self.db.execute(
            query="""INSERT INTO stat_oddluzeni
            (spisovaznacka, zpro_id, zspo_id, vysledek_oddluzeni, n_osvobozeno, z_osvobozeno)
        VALUES
            (:spisovaznacka, :zpro_id, :zspo_id, :vysledek_oddluzeni, :n_osvobozeno, :z_osvobozeno)""",
            values={
                "spisovaznacka": ins_vec["spisovaznacka"],
                "zpro_id": zprava_pro_oddluzeni["doc_id"] if zprava_pro_oddluzeni is not None else None,
                "zspo_id": zprava_splneni_oddluzeni["doc_id"] if zprava_splneni_oddluzeni is not None else None,
                "vysledek_oddluzeni": vysledek_oddluzeni,
                "n_osvobozeno": n_osvobozeno,
                "z_osvobozeno": z_osvobozeno,
            }
        )

    async def run(self):
        i = 0
        rows = await self.seznamInsRizeni()
        while rows:
            for row in rows:
                i += 1
                await self.analyzaPohledavekRizeni(dict(row))
                
            rows = await self.seznamInsRizeni()
            print("Zpracovano {0} ...".format(i))
