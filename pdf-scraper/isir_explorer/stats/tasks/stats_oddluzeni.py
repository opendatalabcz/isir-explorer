from ..task import Task


class StatsOddluzeni(Task):

    DOPORUCENI_OSVOBOZENI = "přiznání osvobození od placení zbývajících pohledávek"
    DOPORUCENI_ZRUSENI = "zrušení schváleného oddlužení"

    MAX_DELTA_DAYS = 10000

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.posledni_spisovaznacka = ""

    async def seznamInsRizeni(self):
        rows = await self.db.fetch_all(query="""
            SELECT iv.*, sv.datum_ukonceni FROM isir_vec iv
                LEFT JOIN stat_oddluzeni so ON (iv.spisovaznacka = so.spisovaznacka)
                LEFT JOIN stat_vec sv ON (sv.spisovaznacka = iv.spisovaznacka)
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
        n_uspokojeni_mira = None
        z_uspokojeni_mira = None
        n_uspokojeni_vs_predpoklad = None
        n_uspokojeni_predpoklad = None
        delka_oddluzeni = None
        delka_zjis_upadku = None
        delka_schvalovani = None
        delka_pred_schvalenim = None
        ukonceni_oddluzeni = None

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

            if zprava_splneni_oddluzeni["n_predpoklad_uspokojeni_mira"] \
                    and zprava_splneni_oddluzeni["n_uspokojeni_mira"]:
                n_uspokojeni_mira = min(100, zprava_splneni_oddluzeni["n_uspokojeni_mira"])
                n_uspokojeni_predpoklad = min(100, zprava_splneni_oddluzeni["n_predpoklad_uspokojeni_mira"])
                n_uspokojeni_vs_predpoklad = n_uspokojeni_mira - n_uspokojeni_predpoklad
            
            if zprava_splneni_oddluzeni["z_uspokojeni_mira"]:
                z_uspokojeni_mira = min(100, zprava_splneni_oddluzeni["z_uspokojeni_mira"])
            
            # Delka oddluzeni
            if zprava_splneni_oddluzeni["posledni_splatka"] and zprava_splneni_oddluzeni["oddluzeni_schvaleno"]:
                delta = zprava_splneni_oddluzeni["posledni_splatka"] - zprava_splneni_oddluzeni["oddluzeni_schvaleno"]
                delka_oddluzeni = delta.days if abs(delta.days) < self.MAX_DELTA_DAYS else None

            # Doba zjistovani upadku
            if zprava_splneni_oddluzeni["zahajeno"] and zprava_splneni_oddluzeni["zjisteni_upadku"]:
                delta = zprava_splneni_oddluzeni["zjisteni_upadku"] - zprava_splneni_oddluzeni["zahajeno"]
                delka_zjis_upadku = delta.days if abs(delta.days) < self.MAX_DELTA_DAYS else None

            # Doba schvaleni oddluzeni
            if zprava_splneni_oddluzeni["oddluzeni_povoleno"] and zprava_splneni_oddluzeni["oddluzeni_schvaleno"]:
                delta = zprava_splneni_oddluzeni["oddluzeni_schvaleno"] - zprava_splneni_oddluzeni["oddluzeni_povoleno"]
                delka_schvalovani = delta.days if abs(delta.days) < self.MAX_DELTA_DAYS else None

            # Celkova doba pred schvalenim oddluzeni
            if zprava_splneni_oddluzeni["zahajeno"] and zprava_splneni_oddluzeni["oddluzeni_schvaleno"]:
                delta = zprava_splneni_oddluzeni["oddluzeni_schvaleno"] - zprava_splneni_oddluzeni["zahajeno"]
                delka_pred_schvalenim = delta.days if abs(delta.days) < self.MAX_DELTA_DAYS else None

            # Datum ukonceni
            if zprava_splneni_oddluzeni["posledni_splatka"]:
                ukonceni_oddluzeni = zprava_splneni_oddluzeni["posledni_splatka"]
            elif zprava_splneni_oddluzeni["zaslani_vyzvy_ukonceni_srazek"]:
                ukonceni_oddluzeni = zprava_splneni_oddluzeni["zaslani_vyzvy_ukonceni_srazek"]

            # Vysledek
            if vysledek_oddluzeni:
                n_osvobozeno = self.osvobozeni(
                    zprava_splneni_oddluzeni["n_uspokojeni_mira"], zprava_splneni_oddluzeni["n_uspokojeni_vyse"])
                z_osvobozeno = self.osvobozeni(
                    zprava_splneni_oddluzeni["z_uspokojeni_mira"], zprava_splneni_oddluzeni["z_uspokojeni_vyse"])

        # Pokud se nepodari najit datum ukonceni ve zspo, pouzit datum z ins_vec
        if not ukonceni_oddluzeni:
            ukonceni_oddluzeni = ins_vec["datum_ukonceni"]

        await self.db.execute(
            query="""INSERT INTO stat_oddluzeni
            (spisovaznacka, zpro_id, zspo_id, vysledek_oddluzeni, n_osvobozeno, z_osvobozeno,
            n_uspokojeni_mira, z_uspokojeni_mira, n_uspokojeni_vs_predpoklad, n_uspokojeni_predpoklad,
            delka_oddluzeni, ukonceni_oddluzeni, delka_zjis_upadku, delka_schvalovani, delka_pred_schvalenim)
        VALUES
            (:spisovaznacka, :zpro_id, :zspo_id, :vysledek_oddluzeni, :n_osvobozeno, :z_osvobozeno,
            :n_uspokojeni_mira, :z_uspokojeni_mira, :n_uspokojeni_vs_predpoklad, :n_uspokojeni_predpoklad,
            :delka_oddluzeni, :ukonceni_oddluzeni, :delka_zjis_upadku, :delka_schvalovani, :delka_pred_schvalenim)""",
            values={
                "spisovaznacka": ins_vec["spisovaznacka"],
                "zpro_id": zprava_pro_oddluzeni["doc_id"] if zprava_pro_oddluzeni is not None else None,
                "zspo_id": zprava_splneni_oddluzeni["doc_id"] if zprava_splneni_oddluzeni is not None else None,
                "vysledek_oddluzeni": vysledek_oddluzeni,
                "n_osvobozeno": n_osvobozeno,
                "z_osvobozeno": z_osvobozeno,
                "n_uspokojeni_mira": n_uspokojeni_mira,
                "z_uspokojeni_mira": z_uspokojeni_mira,
                "n_uspokojeni_vs_predpoklad": n_uspokojeni_vs_predpoklad,
                "n_uspokojeni_predpoklad": n_uspokojeni_predpoklad,
                "ukonceni_oddluzeni": ukonceni_oddluzeni,
                "delka_oddluzeni": delka_oddluzeni,
                "delka_zjis_upadku": delka_zjis_upadku,
                "delka_schvalovani": delka_schvalovani,
                "delka_pred_schvalenim": delka_pred_schvalenim,
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
