from parser.model.zprava_pro_oddluzeni import ZpravaProOddluzeni, PrijemDluznika, ZaznamSoupisuMajetku
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *
import re

class ZpravaProOddluzeniParser(IsirParser):

    def __init__(self, data):
        self.txt = data
        self.lines = data.split('\n')
        self.model = ZpravaProOddluzeni()
        super().__init__()

    def extractDocument(self):
        self.txt = self.reTextBetween(self.txt, "^[\s]*A\. Hospodářská situace dlužníka", "^[\s]*C\. Přílohy")
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

    def _prijmyDluznika(self,txt):
        """Prijmy dluznika

        Ve formuláři se někde vyskytuje "Výše přijmu" namísto "Výše příjmu".

        Args:
            txt (string): Sekce "Hospodářská situace dlužníka"
        """
        
        # Sekce s prijmy dluznika
        txtPrijmy = self.reTextBetween(txt, "^[\s]*PŘÍJEM DLUŽNÍKA č\.", "^[\s]*FINANČNÍ DAR / DŮCHOD / RENTA DLUŽNÍKA")

        # Rozdeleni jednotlivych prijmu
        prijmyParts = self.reSplitText(txtPrijmy, "^[\s]*PŘÍJEM DLUŽNÍKA č\.")

        for txtPrijem in prijmyParts:
            lines = txtPrijem.split('\n')
            prijem = PrijemDluznika()
            for line in lines:
                if self.reMatch(line, '^[\s]*Název plátce příjmu'):
                    prijem.Nazev_platce = self.reTextAfter(line, '^[\s]*Název plátce příjmu')
                elif self.reMatch(line, '^[\s]*Adresa'):
                    prijem.Adresa = self.reTextAfter(line, '^[\s]*Adresa')
                elif self.reMatch(line, '^[\s]*IČO'):
                    prijem.ICO = self.reTextAfter(line, '^[\s]*IČO')
                elif self.reMatch(line, '^[\s]*Typ příjmu'):
                    prijem.Typ = self.reTextAfter(line, '^[\s]*Typ příjmu')
                elif self.reMatch(line, '^[\s]*Výše př.jmu'):
                    prijem.Vyse = self.priceValue(self.reTextAfter(line, '^[\s]*Výše př.jmu'))
            if hasattr(prijem, 'Vyse') and prijem.Vyse != '':
                self.model.Prijmy_dluznika.Prijmy.append(prijem)

        # Renta dluznika
        txtRenta = self.reTextBetween(txt, "^[\s]*FINANČNÍ DAR / DŮCHOD / RENTA DLUŽNÍKA", "^[\s]*Komentář:")
        lines = txtRenta.split('\n')
        prijem = PrijemDluznika()
        for line in lines:
            print(line)
            if self.reMatch(line, '^[\s]*Jméno a příjmení poskytovatele'):
                prijem.Nazev_platce = self.removeSpaces(self.reTextAfter(line, '^[\s]*Jméno a příjmení poskytovatele'))
            elif self.reMatch(line, '^[\s]*Typ příjmu'):
                prijem.Typ = self.reTextAfter(line, '^[\s]*Typ příjmu')
            elif self.reMatch(line, '^[\s]*Výše př.jmu'):
                prijem.Vyse = self.priceValue(self.reTextAfter(line, '^[\s]*Výše př.jmu'))
            if hasattr(prijem, 'Vyse') and prijem.Vyse != '':
                self.model.Prijmy_dluznika.Prijmy.append(prijem)
                prijem = PrijemDluznika()

        # Komentar k prijmum
        self.model.Prijmy_dluznika.Komentar = self.textBlock(self.reTextBetween(txt, "^[\s]*Komentář:", "^[\s]*CELKOVÝ MĚSÍČNÍ PŘÍJEM DLUŽNÍKA"))

        # Celkovy mesicni prijem
        self.model.Prijmy_dluznika.Celkem = self.priceValue(self.reLineTextAfter(txt, "^[\s]*CELKOVÝ MĚSÍČNÍ PŘÍJEM DLUŽNÍKA"))


    def _prehledMajetkovePodstaty(self, txt):
        txtPrehled = self.reTextBetween(txt, "^[\s]*PŘEHLED SOUPISU MAJETKOVÉ PODSTATY DLUŽNÍKA", "^[\s]*HOSPODÁŘSKÁ SITUACE DLUŽNÍKA")
        lines = txtPrehled.split('\n')
        for line in lines:
            parts = re.compile("[\s]{2,}").split(line.strip())
            if len(parts) != 4:
                continue
            zaznam = ZaznamSoupisuMajetku()
            
            zaznam.Oceneni = self.priceValue(parts[1])
            zaznam.Zajisteno = self.priceValue(parts[2])
            zaznam.Nezajisteno = self.priceValue(parts[3])

            if parts[0] == 'Nemovitý majetek':
                self.model.Soupis_majetku.Nemovity = zaznam
            elif parts[0] == 'Movitý majetek':
                self.model.Soupis_majetku.Movity = zaznam
            elif parts[0] == 'Finanční prostředky':
                self.model.Soupis_majetku.Financni_prostredky = zaznam
            elif parts[0] == 'Pohledávky':
                self.model.Soupis_majetku.Pohledavky = zaznam
            elif parts[0] == 'Ostatní majetek':
                self.model.Soupis_majetku.Ostatni = zaznam
            elif parts[0] == 'Celkem':
                self.model.Soupis_majetku.Celkem = zaznam

    def _hospodarskaSituaceDluznika(self):
        txt = self.reTextBetween(self.txt, "^[\s]*A\. Hospodářská situace dlužníka", "^[\s]*B\. Navrhovaný způsob řešení úpadku")

        self._prijmyDluznika(txt)

        self._prehledMajetkovePodstaty(txt)

        # Výše zálohy insolvencniho spravce
        self.model.Hospodarska_situace.Vyse_zalohy = self.priceValue(self.reLineTextAfter(txt, "^[\s]*Výše zálohy"))
        self.model.Hospodarska_situace.Vytezek_zpenezeni_obydli = self.priceValue(self.reLineTextAfter(txt, "^[\s]*Očekávaná výše výtěžku zpeněžení obydlí"))
        self.model.Hospodarska_situace.Povinnen_vydat_obydli = self.reLineTextAfter(txt, "^[\s]*Dlužník povinen vydat obydlí ke zpeněžení")
        self.model.Hospodarska_situace.Zpracovatel_navrhu = self.reLineTextAfter(txt, "^[\s]*Zpracovatel návrhu na povolení oddlužení")
        self.model.Hospodarska_situace.Odmena_za_sapsani_navrhu = self.priceValue(self.reLineTextAfter(txt, "^[\s]*-[\s]*výše odměny za sepsání a podání"))
            

    def _navrhovanyZpusobReseni(self):
        txt = self.reTextBetween(self.txt, "^[\s]*B\. Navrhovaný způsob řešení úpadku", "^[\s]*C\. Přílohy")


    def run(self):
        super().run()

        self._hospodarskaSituaceDluznika()

        self._navrhovanyZpusobReseni()

        #print(self.txt)