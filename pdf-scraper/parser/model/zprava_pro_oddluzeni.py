from parser.model.isir_dokument import IsirDokument

class PrijemDluznika:
    pass

class ZaznamPohledavky():
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
        self.Navrh_reseni = PrehledPohledavek()
        super().__init__()
