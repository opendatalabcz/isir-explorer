from .isir_dokument import IsirDokument

class PrijemDluznika:
    def __init__(self):
        self.Nazev_platce = None
        self.Adresa = None
        self.ICO = None
        self.Typ = None
        self.Vyse = 0

class ZaznamPohledavky():
    pass

class ZaznamSoupisuMajetku:
    def __init__(self):
        self.Oceneni = ""
        self.Zajisteno = ""
        self.Nezajisteno = ""

class SoupisMajetku():
    pass

class PredpokladUspokojeniVeritelu:

    class ZaznamPredpokladuUspokojeni:
        def __init__(self):
            self.Mira = None
            self.Vyse = None

    def __init__(self):
        self.Splatkovy_kalendar = self.ZaznamPredpokladuUspokojeni()
        self.Zpenezeni_majetku = self.ZaznamPredpokladuUspokojeni()
        self.Splat_kal_zpen_maj = self.ZaznamPredpokladuUspokojeni()

class PredpokladUspokojeni:
    pass

class HospodarskaSituace:
    pass

class ZaznamDistribucnihoSchematu:
    def __init__(self):
        self.Veritel = None
        self.Castka = None
        self.Podil = None


class DistribucniSchema():

    def __init__(self):
        self.Nezajistene = []
        self.Zajistene = []

class PrijmyDluznika:

    def __init__(self):
        self.Prijmy = []
        self.Komentar = ""


class ZpravaProOddluzeni(IsirDokument):

    TYP_DOKUMENTU = "ZpravaProOddluzeni"

    def __init__(self):
        self.Prijmy_dluznika = PrijmyDluznika()
        self.Soupis_majetku = SoupisMajetku()
        self.Hospodarska_situace = HospodarskaSituace()
        self.Distribucni_schema = DistribucniSchema()
        self.Predpoklad_uspokojeni = PredpokladUspokojeni()
        super().__init__()
