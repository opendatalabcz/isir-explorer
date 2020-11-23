from .model.prehledovy_list import PrehledovyList, ZaznamPohledavky
from .isir_parser import IsirParser
from .model.parts.osoba import *
from .model.parts.spisova_znacka import *
import re

class PrehledovyListParser(IsirParser):

    def __init__(self, data):
        super().__init__(data)
        self.model = PrehledovyList()

    def extractDocument(self):
        doc_start = "^[\s]*Přezkumné jednání / Přezkum přihlášených pohledávek:"
        doc_end = "^[\s]*[D-H]\. Přílohy"
        self.extractDocumentByRange(doc_start, doc_end)

    def _prehledPohledavek(self, txt):
        """Funkce pro čtení tabulky s přehledem pohledávek. Použití je možné pro sekce
        C. a D. přehledového listu pohledávek (zajištěné a nezajištěné pohledávky).

        Args:
            txt (string): Část textu obsahující tabulku s přehledem

        Returns:
            tuple(pohledavky,celkem): Seznam pohledávek a sumarizace
        """
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

        pohledavky = []
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

            pohledavky.append(zaznam)

        # Radek se sumarizaci ma jine usporadani sloupcu
        celkem = ZaznamPohledavky()
        if len(total) == 2:
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

        return pohledavky, celkem

    def _prehledZajistenych(self):
        txt = self.reTextBetween(self.txt, "^[\s]*B. Přehled přihlášených zajištěných pohledávek", "^[\s]*Komentář:")
        pohledavky, celkem = self._prehledPohledavek(txt)
        self.model.Zajistene.Pohledavky = pohledavky
        self.model.Zajistene.Celkem = celkem

    def _prehledNezajistenych(self):
        txt = self.reTextBetween(self.txt, "^[\s]*C. Přehled přihlášených nezajištěných pohledávek", "^[\s]*Komentář:")
        pohledavky, celkem = self._prehledPohledavek(txt)
        self.model.Nezajistene.Pohledavky = pohledavky
        self.model.Nezajistene.Celkem = celkem

    def run(self):
        super().run()

        # B. Přehled přihlášených zajištěných pohledávek
        self._prehledZajistenych()

        # C. Přehled přihlášených nezajištěných pohledávek
        self._prehledNezajistenych()
