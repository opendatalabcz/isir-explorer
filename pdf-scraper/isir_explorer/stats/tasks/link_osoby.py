import re
from ..task import Task


class LinkOsoby(Task):

    TYP_SPOJENI_OSOBA_NENALEZNA = 0
    TYP_SPOJENI_RC = 1
    TYP_SPOJENI_IC = 2
    TYP_SPOJENI_JMENO_PRIJMENI = 3
    TYP_SPOJENI_OBCHODNI_NAZEV = 4
    TYP_SPOJENI_JMENO_PRIJMENI_PREHOZENO = 5
    TYP_SPOJENI_CASTECNA_PODMNOZINA_NAZVU = 6
    # pouzito v zprave o plneni oddluzeni
    TYP_SPOJENI_CISLO_VERITELE = 7

    def upravaProSrovnani(self, text):
        if text is None:
            return None
        return re.sub('[.,-]', '', text).lower()

    def jePodmnozinou(self, a, b):
        if not a or not b:
            return False
        if len(a) > len(b):
            a, b = b, a
        return set(a).issubset(set(b))

    def jeCastecnouPodmnozinou(self, a, b, pomer_delky=0.75):
        if not a or not b:
            return False
        if len(a) > len(b):
            a, b = b, a
        b_copy = []
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
        self.osobyRizeniCache[spis] = list(map(dict, rows))

        for isir_osoba in self.osobyRizeniCache[spis]:
            isir_osoba["nazevosoby"] = self.upravaProSrovnani(
                isir_osoba["nazevosoby"])
            isir_osoba["jmeno"] = self.upravaProSrovnani(isir_osoba["jmeno"])
            isir_osoba["nazevosoby_slova"] = isir_osoba["nazevosoby"].split(
                " ") if isir_osoba["nazevosoby"] is not None else []
            if isir_osoba["jmeno"] is not None:
                isir_osoba["nazevosoby_slova"] += isir_osoba["jmeno"].split(
                    " ")

        return self.osobyRizeniCache[spis]
