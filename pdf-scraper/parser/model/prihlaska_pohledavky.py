from parser.model.isir_dokument import IsirDokument

class SekcePohledavky():

    def __init__(self):
        self.Pohledavky = []


class PrihlaskaPohledavky(IsirDokument):

    def __init__(self):
        self.Pohledavky = SekcePohledavky()
        super().__init__()
