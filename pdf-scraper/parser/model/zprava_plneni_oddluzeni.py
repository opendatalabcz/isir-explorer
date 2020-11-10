from parser.model.isir_dokument import IsirDokument

class ZpravaSpravce:
    pass

class VykazPlneni:
    pass

class ZpravaPlneniOddluzeni(IsirDokument):

    TYP_DOKUMENTU = "ZpravaPlneniOddluzeni"

    def __init__(self):
        self.ZpravaSpravce = ZpravaSpravce()
        self.VykazPlneni = VykazPlneni()
        super().__init__()
