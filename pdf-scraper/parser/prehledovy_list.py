from parser.model.prehledovy_list import PrehledovyList, ZaznamPohledavky
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *
import re

class PrehledovyListParser(IsirParser):

    def __init__(self, data):
        self.txt = data
        self.lines = data.split('\n')
        self.model = PrehledovyList()
        super().__init__()

    def extractDocument(self):
        self.txt = self.reTextBetween(self.txt, "^[\s]*Přezkumné jednání / Přezkum přihlášených pohledávek:", "^[\s]*[D-H]\. Přílohy")


    def _prehledNezajistenych(self):
        txt = self.reTextBetween(self.txt, "^[\s]*C. Přehled přihlášených nezajištěných pohledávek", "^[\s]*Komentář:")
        lines = txt.split('\n')

        rows = []
        for line in lines:
            line = line.strip()
            if line == '':
                continue

            parts = re.compile("[\s]{2,}").split(line)
            rows.append(parts)

        i = 1
        rowgroups = []
        total = []
        while i < len(rows):
            if len(rows[i]) == 7 and i+1 < len(rows) and len(rows[i+1]) == 7:
                rowgroups.append([rows[i-1], rows[i], rows[i+1]])
                i+=2
                continue
            if len(rows[i])==1 and rows[i][0] == 'Celkem':
                while i < len(rows):
                    if len(rows[i]) == 5:
                        total.append(rows[i])
                    if len(total) == 2:
                        break
                    i+=1
                break
            i+=1

        for rg in rowgroups:
            zaznam = ZaznamPohledavky()
            
            # 1. radek
            zaznam.Veritel = ' '.join(rg[0]).strip(',')

            # 2. radek
            zaznam.Cislo_veritele  = self.numbersOnly(rg[1][0])
            zaznam.Celkova_vyse    = self.priceValue(rg[1][1])
            zaznam.Vykonatelne     = self.priceValue(rg[1][2])
            zaznam.Popreno         = self.priceValue(rg[1][3])
            zaznam.Podmineno       = self.priceValue(rg[1][4])
            zaznam.Neprezkoumavano = self.priceValue(rg[1][5])
            zaznam.Datum_doruceni  = rg[1][6]

            # 3. radek
            zaznam.Cislo_prihlasky = self.numbersOnly(rg[2][0])
            zaznam.Zbyva_uspokojit = self.priceValue(rg[2][1])
            zaznam.Nevykonatelne   = self.priceValue(rg[2][2])
            zaznam.Zjisteno        = self.priceValue(rg[2][3])
            zaznam.Duplicitni      = self.priceValue(rg[2][4])
            zaznam.Odmitnuto       = self.priceValue(rg[2][5])
            zaznam.Procent         = self.priceValue(rg[2][6])

            self.model.Nezajistene.Pohledavky.append(zaznam)

        # Radek se sumarizaci ma jine usporadani sloupcu
        celkem = ZaznamPohledavky()
        celkem.Celkova_vyse      = self.priceValue(total[0][0])
        celkem.Vykonatelne       = self.priceValue(total[0][1])
        celkem.Popreno           = self.priceValue(total[0][2])
        celkem.Podmineno         = self.priceValue(total[0][3])
        celkem.Neprezkoumavano   = self.priceValue(total[0][4])

        celkem.Zbyva_uspokojit   = self.priceValue(total[1][0])
        celkem.Nevykonatelne     = self.priceValue(total[1][1])
        celkem.Zjisteno          = self.priceValue(total[1][2])
        celkem.Duplicitni        = self.priceValue(total[1][3])
        celkem.Odmitnuto         = self.priceValue(total[1][4])

        self.model.Nezajistene.Celkem = celkem


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

    def run(self):
        super().run()

        self._prehledNezajistenych()
        # C. Přehled přihlášených nezajištěných pohledávek
        
        #print(self.txt)
