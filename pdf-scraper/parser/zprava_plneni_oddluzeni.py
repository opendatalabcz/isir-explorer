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

    def _zpravaSpravcePlneni(self):
        txt = self.reTextBefore(self.txt, "^[\s]*B\. MĚSÍČNÍ VÝKAZ PLNĚNÍ SPLÁTKOVÉHO KALENDÁŘE", True)
        self.model.ZpravaSpravce.Plni_povinnosti = self.reLineTextAfter(txt, "^[\s]*Dlužník plní povinnosti v rámci schváleného způsobu oddlužení")
        self.model.ZpravaSpravce.Duvod_neplneni = self.textBlock(self.reTextBetween(txt, "^[\s]*-[\s]*důvod neplnění schváleného způsobu oddlužení:", "^[\s]*-[\s]*stanovisko dlužníka, jak se hodlá vypořádat se vzniklou situací:"))
        self.model.ZpravaSpravce.Stanovisko_dluznika = self.textBlock(self.reTextBetween(txt, "^[\s]*-[\s]*stanovisko dlužníka, jak se hodlá vypořádat se vzniklou situací:", "^[\s]*Vyjádření insolvenčního správce k plnění povinností dlužníka v oddlužení:"))
        self.model.ZpravaSpravce.Vyjadreni_spravce = self.textBlock(self.reTextBetween(txt, "^[\s]*Vyjádření insolvenčního správce k plnění povinností dlužníka v oddlužení:", "^[\s]*Aktuální míra uspokojení nezajištěných věřitelů"))
        
    
    def _mesicniVykazPlneni(self):
        pass

    def run(self):
        super().run()

        self._zpravaSpravcePlneni()

        self._mesicniVykazPlneni()

        #print(self.txt)