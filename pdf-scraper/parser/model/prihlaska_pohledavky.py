from parser.model.isir_dokument import IsirDokument

class PrihlaskaPohledavky(IsirDokument):

    def __init__(self):
        self.Pohledavky = []
        super().__init__()
