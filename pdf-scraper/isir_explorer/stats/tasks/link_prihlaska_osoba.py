import os
import json
import re
from databases import Database

class LinkPrihlaskaOsoba:

    TYP_SPOJENI_OSOBA_NENALEZNA = 0
    TYP_SPOJENI_RC = 1
    TYP_SPOJENI_IC = 2
    TYP_SPOJENI_JMENO_PRIJMENI = 3
    TYP_SPOJENI_OBCHODNI_NAZEV = 4
    TYP_SPOJENI_JMENO_PRIJMENI_PREHOZENO = 5
    TYP_SPOJENI_CASTECNA_PODMNOZINA_NAZVU = 6

    def __init__(self, config, db=None):
        self.config = config
        if db is None:
            self.db = Database(self.config['db.dsn'])
        else:
            self.db = db

        self.osobyRizeniCache = {}
        self.nalezeno = 0
        self.nenalezeno = 0

    def upravaProSrovnani(self, text):
        if text is None:
            return None
        return re.sub('[.,-]', '', text).lower()

    def jeCastecnouPodmnozinou(self, a, b, pomer_delky=0.75):
        if not a or not b:
            return False
        if len(a) > len(b):
            a, b = b, a
        b_copy  = []
        celkovaDelka = 0
        for elB in b:
            b_copy.append(elB)
            celkovaDelka += len(elB)
        for elA in a:
            try:
                b_copy.remove(elA)
            except ValueError:
                pass
        if not b_copy:
            # Uplna shoda
            return True
        pomerDelkyRetezcuPodmnoziny = 1 - len(''.join(b_copy)) / celkovaDelka
        return pomerDelkyRetezcuPodmnoziny > pomer_delky

    async def osobyRizeni(self, spis):
        if spis in self.osobyRizeniCache:
            return self.osobyRizeniCache[spis]

        rows = await self.db.fetch_all(query="""
            SELECT * FROM isir_osoba WHERE spisovaznacka = :spis
        """, values={"spis": spis})

        self.osobyRizeniCache = {}
        self.osobyRizeniCache[spis] = list(map(dict,rows))

        for isir_osoba in self.osobyRizeniCache[spis]:
            isir_osoba["nazevosoby"] = self.upravaProSrovnani(isir_osoba["nazevosoby"])
            isir_osoba["jmeno"] = self.upravaProSrovnani(isir_osoba["jmeno"])
            isir_osoba["nazevosoby_slova"] = isir_osoba["nazevosoby"].split(" ") if isir_osoba["nazevosoby"] is not None else []
            if isir_osoba["jmeno"] is not None:
                isir_osoba["nazevosoby_slova"] += isir_osoba["jmeno"].split(" ")

        return self.osobyRizeniCache[spis]

    async def spojitOsobu(self, typ_spojeni, isir_osoba_id, pp_osoba_id):
        await self.db.execute(query="""
            UPDATE pp_osoba SET isir_osoba=:isir_osoba_id, osoba_spojena=:osoba_spojena WHERE id=:pp_osoba_id
        """, values={
            "osoba_spojena": typ_spojeni,
            "isir_osoba_id": isir_osoba_id,
            "pp_osoba_id": pp_osoba_id,
        })

    async def najitSpojeniOsoby(self, hledana_osoba, osoby_rizeni):
        hledana_osoba["nazevosoby"] = self.upravaProSrovnani(hledana_osoba["nazevosoby"])
        hledana_osoba["jmeno"] = self.upravaProSrovnani(hledana_osoba["jmeno"])
        hledana_osoba["nazevosoby_slova"] = hledana_osoba["nazevosoby"].split(" ") if hledana_osoba["nazevosoby"] is not None else None
        if hledana_osoba["jmeno"] is not None:
                hledana_osoba["nazevosoby_slova"] += hledana_osoba["jmeno"].split(" ")

        for isir_osoba in osoby_rizeni:

            if hledana_osoba["ic"]:
                if hledana_osoba["ic"] == isir_osoba["ic"]:
                    return isir_osoba, self.TYP_SPOJENI_IC

            if hledana_osoba["rc"]:
                if hledana_osoba["rc"] == isir_osoba["rc"]:
                    return isir_osoba, self.TYP_SPOJENI_RC

            if hledana_osoba["jmeno"] and isir_osoba["jmeno"] and hledana_osoba["nazevosoby"]:
                if hledana_osoba["jmeno"] == isir_osoba["jmeno"] and \
                        hledana_osoba["nazevosoby"] == isir_osoba["nazevosoby"]:
                    return isir_osoba, self.TYP_SPOJENI_JMENO_PRIJMENI

            if 3 == hledana_osoba["druhosoby"] and hledana_osoba["nazevosoby"]:
                if isir_osoba["druhosoby"] != 1 and \
                    hledana_osoba["nazevosoby"] == isir_osoba["nazevosoby"]:
                    return isir_osoba, self.TYP_SPOJENI_OBCHODNI_NAZEV

            if hledana_osoba["jmeno"] and isir_osoba["jmeno"] and hledana_osoba["nazevosoby"]:
                if hledana_osoba["nazevosoby"] == isir_osoba["jmeno"] and \
                        hledana_osoba["jmeno"] == isir_osoba["nazevosoby"]:
                    return isir_osoba, self.TYP_SPOJENI_JMENO_PRIJMENI_PREHOZENO

        kandidat = []
        for isir_osoba in osoby_rizeni:
            if self.jeCastecnouPodmnozinou(isir_osoba["nazevosoby_slova"], hledana_osoba["nazevosoby_slova"]):
                kandidat.append(isir_osoba)
        if len(kandidat) == 1:
            return kandidat[0], self.TYP_SPOJENI_CASTECNA_PODMNOZINA_NAZVU

        return None, self.TYP_SPOJENI_OSOBA_NENALEZNA

    async def seznamNeprirazenychOsob(self):
        return await self.db.fetch_all(query="""
                SELECT *, pp_osoba.id AS pp_osoba_id FROM pp_osoba
                    LEFT JOIN pp_osoba_sidlo sidlo ON (sidlo.osoba_id = pp_osoba.id)
                    LEFT JOIN dokument ON (dokument.id = pp_osoba.pp_id)
                WHERE
                    pp_osoba.osoba_spojena IS NULL AND
                    pp_osoba.druhrolevrizeni = 3
                ORDER BY dokument.spisova_znacka ASC
                LIMIT 5000
            """)

    async def run(self):
        rows = await self.seznamNeprirazenychOsob()
        while rows:
            for row in rows:
                hledana_osoba = dict(row)
                osoby_rizeni = await self.osobyRizeni(hledana_osoba["spisova_znacka"])
                nalezena_osoba, typ_spojeni = await self.najitSpojeniOsoby(hledana_osoba, osoby_rizeni)
                if nalezena_osoba:
                    await self.spojitOsobu(typ_spojeni, nalezena_osoba["id"], hledana_osoba["pp_osoba_id"])
                    self.nalezeno += 1
                else:
                    await self.spojitOsobu(typ_spojeni, None, hledana_osoba["pp_osoba_id"])
                    self.nenalezeno += 1
            rows = await self.seznamNeprirazenychOsob()
            print("Zpracovano {0} ...".format(self.nenalezeno + self.nalezeno))

        print("Celkem: {0}".format(self.nenalezeno + self.nalezeno))
        print("Spojeno: {0}".format(self.nalezeno))
        print("Nespojeno: {0}".format(self.nenalezeno))