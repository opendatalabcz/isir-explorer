from parser.model.isir_dokument import IsirDokument

class ZaznamPohledavky():
    pass

class PrehledPohledavek():

    def __init__(self):
        self.Pohledavky = []
        self.Celkem = ZaznamPohledavky()


class PrehledovyList(IsirDokument):

    TYP_DOKUMENTU = "PrehledovyList"

    def __init__(self):
        self.Zajistene = PrehledPohledavek()
        self.Nezajistene = PrehledPohledavek()
        super().__init__()
