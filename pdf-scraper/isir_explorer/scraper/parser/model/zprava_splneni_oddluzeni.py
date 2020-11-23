from .isir_dokument import IsirDokument

class PrubehRizeni:
    pass

class VysledekhRizeni:
    pass

class OdmenaSpravce:
    pass

class ZpravaSplneniOddluzeni(IsirDokument):

    TYP_DOKUMENTU = "ZpravaSplneniOddluzeni"

    def __init__(self):
        super().__init__()

        self.Prubeh_rizeni = PrubehRizeni()
        self.Vysledek_rizeni = VysledekhRizeni()
        self.Odmena_spravce = OdmenaSpravce()
