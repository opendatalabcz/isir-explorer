import re
from .link_osoby import LinkOsoby


class LinkVykazPrerozdeleniVeritel(LinkOsoby):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.osobyRizeniCache = {}
        self.nalezeno = 0
        self.nenalezeno = 0

    async def spojitOsobu(self, typ_spojeni, isir_osoba_id, zplo_vykaz_id):
        await self.db.execute(query="""
            UPDATE zplo_vykaz_prerozdeleni_veritel
            SET veritel_id=:isir_osoba_id, osoba_spojena=:osoba_spojena
            WHERE id=:zplo_vykaz_id
        """, values={
            "osoba_spojena": typ_spojeni,
            "isir_osoba_id": isir_osoba_id,
            "zplo_vykaz_id": zplo_vykaz_id,
        })

    def plneniOddluzeniPrefix(self, hledana_osoba):
        nazev = hledana_osoba["veritel"]
        hledana_osoba["cislo_veritele"] = None

        matchFull = re.match("^(\d+)-\d+\s(.*)$", nazev)
        matchSimple = re.match("^(\d+)\s(.*)$", nazev)
        if matchFull:
            hledana_osoba["cislo_veritele"] = int(matchFull[1])
            nazev = matchFull[2]
        elif matchSimple:
            nazev = matchSimple[2]

        hledana_osoba["nazevosoby"] = nazev

        return hledana_osoba

    async def najitSpojeniOsoby(self, hledana_osoba, osoby_rizeni):
        hledana_osoba = self.plneniOddluzeniPrefix(hledana_osoba)
        hledana_osoba["nazevosoby"] = self.upravaProSrovnani(
            hledana_osoba["nazevosoby"])
        hledana_osoba["nazevosoby_slova"] = hledana_osoba["nazevosoby"].split(
            " ")

        for isir_osoba in osoby_rizeni:

            if isir_osoba["ic"]:
                if isir_osoba["ic"] in hledana_osoba["nazevosoby_slova"]:
                    return isir_osoba, self.TYP_SPOJENI_IC

            if hledana_osoba["cislo_veritele"] == isir_osoba["cislo_veritele"]:
                return isir_osoba, self.TYP_SPOJENI_CISLO_VERITELE

        pocetSlov = len(isir_osoba["nazevosoby_slova"])
        j = min(5, pocetSlov)
        for i in range(j):
            kandidat = []
            for isir_osoba in osoby_rizeni:
                if self.jePodmnozinou(isir_osoba["nazevosoby_slova"], hledana_osoba["nazevosoby_slova"]):
                    kandidat.append(isir_osoba)
            if len(kandidat) == 1:
                return kandidat[0], self.TYP_SPOJENI_CASTECNA_PODMNOZINA_NAZVU
            elif len(kandidat) > 1:
                break

        return None, self.TYP_SPOJENI_OSOBA_NENALEZNA

    async def seznamNeprirazenychOsob(self):
        return await self.db.fetch_all(query="""
                SELECT *, v.id AS zplo_vykaz_id FROM zplo_vykaz_prerozdeleni_veritel v
                    LEFT JOIN dokument ON (dokument.id = v.zplo_id)
                WHERE
                    v.osoba_spojena IS NULL
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
                    await self.spojitOsobu(typ_spojeni, nalezena_osoba["id"], hledana_osoba["zplo_vykaz_id"])
                    self.nalezeno += 1
                else:
                    await self.spojitOsobu(typ_spojeni, None, hledana_osoba["zplo_vykaz_id"])
                    self.nenalezeno += 1
            rows = await self.seznamNeprirazenychOsob()
            print("Zpracovano {0} ...".format(self.nenalezeno + self.nalezeno))

        print("Celkem: {0}".format(self.nenalezeno + self.nalezeno))
        print("Spojeno: {0}".format(self.nalezeno))
        print("Nespojeno: {0}".format(self.nenalezeno))
