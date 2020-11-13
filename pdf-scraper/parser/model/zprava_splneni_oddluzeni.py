from parser.model.isir_dokument import IsirDokument

class PrubehRizeni:
    pass

class ZpravaSplneniOddluzeni(IsirDokument):

    TYP_DOKUMENTU = "ZpravaSplneniOddluzeni"

    def __init__(self):
        super().__init__()

        self.Prubeh_rizeni = PrubehRizeni()
