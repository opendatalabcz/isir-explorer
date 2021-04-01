from ..task import Task


class StatsPohledavky(Task):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.init()

    def init(self):
        self.pohledavky_pocet = 0
        self.pocet_nezajistenych = 0
        self.pocet_zajistenych = 0
        self.pocet_splatna = 0
        self.pocet_podrizena = 0
        self.pocet_vykonatelna = 0
        self.pocet_v_cizi_mene = 0
        self.pocet_penezita = 0

        self.vykonatelne = None
        self.nevykonatelne = None
        self.duplicitni = None
        self.neprezkoumavano = None
        self.odmitnuto = None
        self.podmineno = None
        self.popreno = None
        self.zbyva_uspokojit = None
        self.zjisteno = None

        self.celkova_vyse = None
        self.celkova_vyse_nezajistenych = None
        self.celkova_vyse_zajistenych = None

    async def seznamInsRizeni(self):
        return await self.db.fetch_all(query="""
            SELECT iv.* FROM isir_vec iv
                LEFT JOIN stat_pohledavky sp ON (iv.spisovaznacka = sp.spisovaznacka)
            WHERE
                sp.id IS NULL AND
                NOT iv.vyrazeno
            LIMIT 5000
        """)

    async def analyzaPrehledovehoListu(self, ins_vec):
        # Najit nejaktualnejsi verzi prehledoveho listu pro toto rizeni
        prehled_list = await self.db.fetch_one(query="""
            SELECT prehledovy_list.* FROM dokument
            LEFT JOIN prehledovy_list ON prehledovy_list.id = dokument.id
            WHERE dokument.typ = 2 AND spisova_znacka = :spisovaznacka
            ORDER BY dokument.datum DESC LIMIT 1
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})
        if not prehled_list or not prehled_list["id"]:
            return

        self.celkova_vyse = (prehled_list["n_celkova_vyse"] or 0) + (prehled_list["z_celkova_vyse"] or 0)
        self.celkova_vyse_nezajistenych = (prehled_list["n_celkova_vyse"] or 0)
        self.celkova_vyse_zajistenych = (prehled_list["z_celkova_vyse"] or 0)

        self.vykonatelne = (prehled_list["n_vykonatelne"] or 0) + (prehled_list["z_vykonatelne"] or 0)
        self.nevykonatelne = (prehled_list["n_nevykonatelne"] or 0) + (prehled_list["z_nevykonatelne"] or 0)
        self.duplicitni = (prehled_list["n_duplicitni"] or 0) + (prehled_list["z_duplicitni"] or 0)
        self.neprezkoumavano = (prehled_list["n_neprezkoumavano"] or 0) + (prehled_list["z_neprezkoumavano"] or 0)
        self.odmitnuto = (prehled_list["n_odmitnuto"] or 0) + (prehled_list["z_odmitnuto"] or 0)
        self.podmineno = (prehled_list["n_podmineno"] or 0) + (prehled_list["z_podmineno"] or 0)
        self.popreno = (prehled_list["n_popreno"] or 0) + (prehled_list["z_popreno"] or 0)
        self.zbyva_uspokojit = (prehled_list["n_zbyva_uspokojit"] or 0) + (prehled_list["z_zbyva_uspokojit"] or 0)
        self.zjisteno = (prehled_list["n_zjisteno"] or 0) + (prehled_list["z_zjisteno"] or 0)

    def analyzaPohledavek(self, pohledavky):
        self.pohledavky_pocet = len(pohledavky)
        for p in pohledavky:
            if p["typ"] in [1, 2, 4]:
                self.pocet_nezajistenych += 1
            else:
                self.pocet_zajistenych += 1
            self.pocet_splatna += int(p["splatna"] or 0)
            self.pocet_podrizena += int(p["podrizena"] or 0)
            self.pocet_vykonatelna += int(p["vykonatelnost"] or 0)
            self.pocet_v_cizi_mene += int(p["v_cizi_mene"] or 0)
            self.pocet_penezita += int(p["penezita"] or 0)

    async def analyzaPohledavekRizeni(self, ins_vec):
        self.init()

        pocet_prihlasek = await self.db.fetch_one(query="""
            SELECT
                COUNT(*) AS c,
                SUM(celkova_vyse) AS celkova_vyse,
                SUM(celkova_vyse_nezajistenych) AS celkova_vyse_nezajistenych,
                SUM(celkova_vyse_zajistenych) AS celkova_vyse_zajistenych
            FROM dokument
            LEFT JOIN prihlaska_pohledavky pp ON (pp.id = dokument.id)
            WHERE typ = 1 AND spisova_znacka = :spisovaznacka
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})

        if pocet_prihlasek["c"] > 0:
            self.celkova_vyse = pocet_prihlasek["celkova_vyse"]
            self.celkova_vyse_nezajistenych = pocet_prihlasek["celkova_vyse_nezajistenych"]
            self.celkova_vyse_zajistenych = pocet_prihlasek["celkova_vyse_zajistenych"]

        pohledavky = await self.db.fetch_all(query="""
            SELECT pp_pohledavka.* FROM dokument
            LEFT JOIN pp_pohledavka ON (pp_pohledavka.pp_id = dokument.id)
            WHERE dokument.typ = 1 AND dokument.spisova_znacka = :spisovaznacka
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})
        self.analyzaPohledavek(pohledavky)

        await self.analyzaPrehledovehoListu(ins_vec)

        # Preskocit zapis pokud nejsou evidovana zadna data
        if self.celkova_vyse is None:
            return

        await self.db.execute(
            query="""INSERT INTO stat_pohledavky
            (spisovaznacka, prihlasky_pocet, pohledavky_pocet, pocet_nezajistenych, pocet_zajistenych,
            pocet_splatna, pocet_podrizena, pocet_vykonatelna, pocet_v_cizi_mene, pocet_penezita, celkova_vyse,
            celkova_vyse_nezajistenych, celkova_vyse_zajistenych, vykonatelne, nevykonatelne,
            duplicitni, neprezkoumavano, odmitnuto, podmineno, popreno, zbyva_uspokojit, zjisteno)
        VALUES
            (:spisovaznacka, :prihlasky_pocet, :pohledavky_pocet, :pocet_nezajistenych, :pocet_zajistenych,
            :pocet_splatna, :pocet_podrizena, :pocet_vykonatelna, :pocet_v_cizi_mene, :pocet_penezita, :celkova_vyse,
            :celkova_vyse_nezajistenych, :celkova_vyse_zajistenych, :vykonatelne, :nevykonatelne,
            :duplicitni, :neprezkoumavano, :odmitnuto, :podmineno, :popreno, :zbyva_uspokojit, :zjisteno)""",
            values={
                "spisovaznacka": ins_vec["spisovaznacka"],
                "prihlasky_pocet": pocet_prihlasek["c"],
                "pohledavky_pocet": self.pohledavky_pocet,
                "pocet_nezajistenych": self.pocet_nezajistenych,
                "pocet_zajistenych": self.pocet_zajistenych,
                "pocet_splatna": self.pocet_splatna,
                "pocet_podrizena": self.pocet_podrizena,
                "pocet_vykonatelna": self.pocet_vykonatelna,
                "pocet_v_cizi_mene": self.pocet_v_cizi_mene,
                "pocet_penezita": self.pocet_penezita,

                "celkova_vyse": self.celkova_vyse,
                "celkova_vyse_nezajistenych": self.celkova_vyse_nezajistenych,
                "celkova_vyse_zajistenych": self.celkova_vyse_zajistenych,

                "vykonatelne": self.vykonatelne,
                "nevykonatelne": self.nevykonatelne,
                "duplicitni": self.duplicitni,
                "neprezkoumavano": self.neprezkoumavano,
                "odmitnuto": self.odmitnuto,
                "podmineno": self.podmineno,
                "popreno": self.popreno,
                "zbyva_uspokojit": self.zbyva_uspokojit,
                "zjisteno": self.zjisteno,
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
