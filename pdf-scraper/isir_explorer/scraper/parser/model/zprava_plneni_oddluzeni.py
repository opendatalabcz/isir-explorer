from .isir_dokument import IsirDokument


class MiraUspokojeni:
    pass


class ZpravaSpravce:
    def __init__(self):
        self.Mira_uspokojeni = MiraUspokojeni()


class ZaznamVykazuPlneni:

    def __init__(self):
        self.Celkem_prerozdeleno = None
        self.Mira_uspokojeni = None
        self.Mira_uspkojeni_ocekavana = None
        self.Mesic_oddluzeni = None


class ZaznamUspokojeniVeritele:

    def __init__(self):
        self.Veritel = None
        self.Podil = None
        self.Castka = None
        self.Vyplaceno = []


class VykazPlneni:
    def __init__(self):
        self.Mesic = []
        self.Rozdeleni = []


class ZpravaPlneniOddluzeni(IsirDokument):

    TYP_DOKUMENTU = "ZpravaPlneniOddluzeni"

    def __init__(self):
        self.ZpravaSpravce = ZpravaSpravce()
        self.VykazPlneni = VykazPlneni()
        super().__init__()
