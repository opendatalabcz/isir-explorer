from parser.model.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeni
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *
import re

class ZpravaPlneniOddluzeniParser(IsirParser):

    def __init__(self, data):
        self.txt = data
        self.lines = data.split('\n')
        self.model = ZpravaPlneniOddluzeni()
        super().__init__()

    def extractDocument(self):
        self.txt = self.reTextBetween(self.txt, "^[\s]*A\. ZPRÁVA INSOLVENČNÍHO SPRÁVCE O PLNĚNÍ POVINNOSTÍ DLUŽNÍKA V ODDLUŽENÍ", "^[\s]*C\. Přílohy")
        self.lines = self.txt.split('\n')

    def removeVersionLine(self):
        temp = []
        for line in self.lines:
            res = re.match('^[\s]{10,}(?:Stránka [0-9]+ z [0-9]+)?[\s]{5,}Verze ([A-Za-z0-9\-]+)$', line)
            if res:
                # Ulozit verzi pokud jeste neni nastavena
                if self.model.Metadata.Verze is None:
                    self.model.Metadata.Verze = res[1]
            else:
                temp.append(line)
        self.lines = temp
        self.txt = '\n'.join(temp)

    def __zpravaSpravcePlneni(self):
        pass
    
    def _mesicniVykazPlneni(self):
        pass

    def run(self):
        super().run()

        self._zpravaSpravcePlneni()

        self._mesicniVykazPlneni()

        #print(self.txt)