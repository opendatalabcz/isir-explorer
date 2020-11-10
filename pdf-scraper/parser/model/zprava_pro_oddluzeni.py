from parser.model.isir_dokument import IsirDokument

class PrijemDluznika:
    pass

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

class PrehledPohledavek():

    def __init__(self):
        self.Pohledavky = []
        self.Celkem = ZaznamPohledavky()

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
        self.Navrh_reseni = PrehledPohledavek()
        self.Predpoklad_uspokojeni = PredpokladUspokojeni()
        super().__init__()
