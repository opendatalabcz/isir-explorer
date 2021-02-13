from .isir_dokument import IsirDokument


class SekcePohledavky():

    def __init__(self):
        self.Pohledavky = []


class PrihlaskaPohledavky(IsirDokument):

    TYP_DOKUMENTU = "PrihlaskaPohledavky"

    def __init__(self):
        self.Pohledavky = SekcePohledavky()
        super().__init__()
