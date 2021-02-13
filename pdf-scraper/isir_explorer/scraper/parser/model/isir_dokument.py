import json


class DokumentMetadata:
    def __init__(self):
        self.Verze = None


class IsirDokument:

    TYP_DOKUMENTU = "NeznamyTyp"

    def __init__(self):
        super().__init__()
        self.Metadata = DokumentMetadata()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def toDict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))

    def setSoud(self, nazev, znacka):

        self.Insolvencni_soud = {
            "Nazev_soudu": nazev,
            "Spisova_znacka": znacka
        }
