import os
import json
import re
from databases import Database
from ..task import Task
from .link_osoby import LinkOsoby

class LinkPrihlaskaOsoba(LinkOsoby):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.osobyRizeniCache = {}
        self.nalezeno = 0
        self.nenalezeno = 0

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