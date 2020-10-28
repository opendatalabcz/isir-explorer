import json


class IsirDokument:

    def __init__(self):
        super().__init__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def setSoud(self, nazev, znacka):

        self.Insolvencni_soud = {
            "Nazev_soudu": nazev,
            "Spisova_znacka": znacka
        }

