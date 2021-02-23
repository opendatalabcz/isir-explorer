from ..task import Task
from isir_explorer.webservice.enums import DRUH_OSOBY, DRUH_STAV_RIZENI, DRUH_STAV_RIZENI_INV
from .utils.adresa_kraj import AdresaKraj


class StatsInsVec(Task):

    ZPUSOBY_RESENI_UPADKU = [
        DRUH_STAV_RIZENI["KONKURS"],
        DRUH_STAV_RIZENI["ODDLUŽENÍ"],
        DRUH_STAV_RIZENI["REORGANIZ"],
    ]

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.AdresaKraj = AdresaKraj()

    async def seznamInsRizeni(self):
        return await self.db.fetch_all(query="""
            SELECT iv.* FROM isir_vec iv
                LEFT JOIN stat_vec sv ON (iv.spisovaznacka = sv.spisovaznacka)
            WHERE
                sv.id IS NULL AND
                NOT iv.vyrazeno
            LIMIT 5000
        """)

    async def ignorovatRizeni(self, ins_vec):
        await self.db.execute(
            query="""UPDATE isir_vec SET vyrazeno=True WHERE spisovaznacka = :spisovaznacka""", values={
                "spisovaznacka": ins_vec["spisovaznacka"],
            })

    async def analyzaStavu(self, ins_vec):
        stavy_rizeni = await self.db.fetch_all(query="""
            SELECT * FROM isir_vec_stav
            WHERE
                spisovaznacka = :spisovaznacka
            ORDER BY id ASC
        """, values={
            "spisovaznacka": ins_vec["spisovaznacka"],
        })
        
        moratorium = None
        datum_upadek = None
        datum_skonceni = None
        zpusob_reseni = None
        datum_zpusob_reseni = None
        for stav in stavy_rizeni:
            
            if stav["druhstavrizeni"] == DRUH_STAV_RIZENI["MYLNÝ ZÁP."]:
                return None

            elif not datum_upadek and stav["druhstavrizeni"] == DRUH_STAV_RIZENI["ÚPADEK"]:
                datum_upadek = stav["datum"]
            
            elif not datum_skonceni and stav["druhstavrizeni"] == DRUH_STAV_RIZENI["ODSKRTNUTA"]:
                datum_skonceni = stav["datum"]

            elif not zpusob_reseni and stav["druhstavrizeni"] in self.ZPUSOBY_RESENI_UPADKU:
                datum_zpusob_reseni = stav["datum"]
                zpusob_reseni = DRUH_STAV_RIZENI_INV[stav["druhstavrizeni"]][:1]

            elif zpusob_reseni and not datum_skonceni and stav["druhstavrizeni"] == DRUH_STAV_RIZENI["VYRIZENA"]:
                datum_skonceni = stav["datum"]

            elif not moratorium and stav["druhstavrizeni"] == DRUH_STAV_RIZENI["MORATORIUM"]:
                moratorium = stav["datum"]

        return {
            "moratorium": moratorium,
            "datum_upadek": datum_upadek,
            "datum_skonceni": datum_skonceni,
            "zpusob_reseni": zpusob_reseni,
            "datum_zpusob_reseni": datum_zpusob_reseni,
        }

    async def analyzaRizeni(self, ins_vec):

        # Nalezeni prvni udalosti k danemu rizeni
        prvni_udalost = await self.db.fetch_one(query="""
            SELECT MIN(datumzalozeniudalosti) AS datum FROM isir_udalost WHERE
                spisovaznacka = :spisovaznacka AND
                datumzalozeniudalosti IS NOT NULL
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})
        if not prvni_udalost or not prvni_udalost["datum"]:
            await self.ignorovatRizeni(ins_vec)
            return
        datum_zahajeni = prvni_udalost["datum"].date()

        # Informace o dluznikovi
        dluznik = await self.db.fetch_one(query="""
            SELECT * FROM isir_osoba io
            WHERE
                druhrolevrizeni = '1' AND
                spisovaznacka = :spisovaznacka
            ORDER BY datumosobavevecizrusena DESC LIMIT 1
        """, values={"spisovaznacka": ins_vec["spisovaznacka"]})
        if not dluznik:
            await self.ignorovatRizeni(ins_vec)
            return

        typ_osoby = None
        podnikatel = None
        pohlavi_dluznika = None
        if dluznik["druhosoby"] == DRUH_OSOBY["P"]:
            typ_osoby = "P"
            podnikatel = True
        elif dluznik["druhosoby"] == DRUH_OSOBY["F"]:
            typ_osoby = "F"
            podnikatel = False
        elif dluznik["druhosoby"] == DRUH_OSOBY["PODNIKATEL"]:
            typ_osoby = "F"
            podnikatel = True

        # Vek dluznika
        vek_dluznika = None
        if "F" == typ_osoby and dluznik["datumnarozeni"]:
            delta = datum_zahajeni - dluznik["datumnarozeni"]
            vek_dluznika = round(delta.days / 365)

        # Pohlavi dluznika (odhad)
        if "F" == typ_osoby and dluznik["nazevosoby"]:
            pohlavi_dluznika = "M"
            if dluznik["nazevosoby"][-3:] in ["ová", "ova"]:
                pohlavi_dluznika = "Z"

        # Adresa a Kraj dluznika
        adresa_dluznika = await self.db.fetch_one(query="""
            SELECT psc, mesto FROM isir_adresa ia
            WHERE
                ia.idosoby = :idosoby AND
                ia.spisovaznacka = :spisovaznacka AND
                (ia.zeme IS NULL OR ia.zeme IN ('Česká republika','Česko','CZ','CZE','ČR'))
            ORDER BY druhadresy DESC, id ASC LIMIT 1
        """, values={"idosoby": dluznik["idosoby"], "spisovaznacka": ins_vec["spisovaznacka"]})
        if not adresa_dluznika or (not adresa_dluznika["mesto"] and not adresa_dluznika["psc"]):
            kraj = None
        else:
            mesto = adresa_dluznika["mesto"]
            psc = adresa_dluznika["psc"]
            kraj = self.AdresaKraj.najitKraj(psc, mesto)

        data_stavy = await self.analyzaStavu(ins_vec)
        if not data_stavy:
            # Preskocit mylny zapis
            await self.ignorovatRizeni(ins_vec)
            return
        delka_rizeni = None
        if data_stavy["datum_skonceni"]:
            delta = data_stavy["datum_skonceni"].date() - datum_zahajeni
            delka_rizeni = delta.days

        await self.db.execute(query="""INSERT INTO stat_vec
            (spisovaznacka, typ_osoby, podnikatel, datum_zahajeni,
            vek_dluznika, pohlavi_dluznika, kraj, okres, moratorium, datum_upadku,
            datum_zpusob_reseni, datum_ukonceni, typ_rizeni, delka_rizeni)
        VALUES
            (:spisovaznacka, :typ_osoby, :podnikatel, :datum_zahajeni,
            :vek_dluznika, :pohlavi_dluznika, :kraj, :okres, :moratorium, :datum_upadku,
            :datum_zpusob_reseni, :datum_ukonceni, :typ_rizeni, :delka_rizeni)""", values={
                "spisovaznacka": ins_vec["spisovaznacka"],
                "typ_osoby": typ_osoby,
                "podnikatel": podnikatel,
                "datum_zahajeni": datum_zahajeni,
                "vek_dluznika": vek_dluznika,
                "pohlavi_dluznika": pohlavi_dluznika,
                "kraj": kraj["kraj"] if kraj is not None else None,
                "okres": kraj["okres"] if kraj is not None else None,
                "moratorium": data_stavy["moratorium"],
                "datum_upadku": data_stavy["datum_upadek"],
                "datum_zpusob_reseni": data_stavy["datum_zpusob_reseni"],
                "datum_ukonceni": data_stavy["datum_skonceni"],
                "typ_rizeni": data_stavy["zpusob_reseni"],
                "delka_rizeni": delka_rizeni,
            })

    async def run(self):
        i = 0
        rows = await self.seznamInsRizeni()
        while rows:
            for row in rows:
                i += 1
                await self.analyzaRizeni(dict(row))
                
            rows = await self.seznamInsRizeni()
            print("Zpracovano {0} ...".format(i))
