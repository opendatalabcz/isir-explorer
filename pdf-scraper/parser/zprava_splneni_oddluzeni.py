from parser.model.zprava_splneni_oddluzeni import ZpravaSplneniOddluzeni
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *
import re

class ZpravaSplneniOddluzeniParser(IsirParser):

    def __init__(self, data):
        self.txt = data
        self.lines = data.split('\n')
        self.model = ZpravaSplneniOddluzeni()

        super().__init__()

    def extractDocument(self):
        self.txt = self.reTextBetween(self.txt, "^[\s]*A\. Průběh insolvenčního řízení", "^[\s]*F\. Přílohy")
        self.lines = self.txt.split('\n')

    def removeVersionLine(self):
        temp = []
        for line in self.lines:
            res = re.match('^[\s]{10,}(?:Stránka [0-9]+ z [0-9]+)?[\s]+Verze ([A-Za-z0-9\-]+)$', line)
            if res:
                # Ulozit verzi pokud jeste neni nastavena
                if self.model.Metadata.Verze is None:
                    self.model.Metadata.Verze = res[1]
            else:
                temp.append(line)
        self.lines = temp
        self.txt = '\n'.join(temp)

    def _prubehRizeni(self):
        txt = self.reTextBetween(self.txt, "^[\s]*A\. Průběh insolvenčního řízení", "^[\s]*B\. Výsledek insolvenčního řízení")
        
        self.model.Prubeh_rizeni.Zahajeno = self.reLineTextAfter(txt, "^[\s]*Insolvenční řízení zahájeno dne")
        self.model.Prubeh_rizeni.Zjisteni_upadku = self.reLineTextAfter(txt, "^[\s]*Úpadek dlužníka zjištěn usnesením ze dne")
        self.model.Prubeh_rizeni.Oddluzeni_povoleno = self.reLineTextAfter(txt, "^[\s]*Oddlužení povoleno usnesením ze dne")
        self.model.Prubeh_rizeni.Oddluzeni_schvaleno = self.reLineTextAfter(txt, "^[\s]*Oddlužení schváleno usnesením ze dne")

    def _vysledekRizeni(self):
        txt = self.reTextBetween(self.txt, "^[\s]*B\. Výsledek insolvenčního řízení", "^[\s]*C\. Pohledávky za majetkovou podstatou")
        
        self.model.Vysledek_rizeni.Posledni_splatka = self.reLineTextAfter(txt, "^[\s]*Poslední splátka dle splátkového kalendáře")
        self.model.Vysledek_rizeni.Preplatek = self.priceValue(self.reLineTextAfter(txt, "^[\s]*Přeplatek na splátkách ve výši"))

        lines = txt.split('\n')
        
        # Cisla stavu pro detekci hodnot nachazejicich se na jinych radkach, nez jejich nadpisy
        USPOKOJENI_NEZAJ = 1
        ZASLANI_VYZVY = 2

        nextLineState = 0
        for line in lines:
            if self.reMatch(line, '^[\s]*Předpokládaná míra uspokojení nezajištěných'):
                nextLineState = USPOKOJENI_NEZAJ
                continue
            elif self.reMatch(line, '^[\s]*Nezajištění věřitelé uspokojeni \(výše / míra\)'):
                row = self.reTextAfter(line, '^[\s]*Nezajištění věřitelé uspokojeni \(výše / míra\)')
                cols = re.compile("[\s]{2,}").split(row.strip())
                if len(cols) == 2:
                    self.model.Vysledek_rizeni.Uspokojeni_nezaj_vyse = self.priceValue(cols[0])
                    self.model.Vysledek_rizeni.Uspokojeni_nezaj_mira = self.priceValue(cols[1])
                continue
            elif self.reMatch(line, '^[\s]*Zajištění věřitelé uspokojeni \(výše / míra\)'):
                row = self.reTextAfter(line, '^[\s]*Zajištění věřitelé uspokojeni \(výše / míra\)')
                cols = re.compile("[\s]{2,}").split(row.strip())
                if len(cols) == 2:
                    self.model.Vysledek_rizeni.Uspokojeni_zaj_vyse = self.priceValue(cols[0])
                    self.model.Vysledek_rizeni.Uspokojeni_zaj_mira = self.priceValue(cols[1])
                continue
            elif self.reMatch(line, '^[\s]*Plátci příjmu zaslána výzva k ukončení provádění srážek'):
                nextLineState = ZASLANI_VYZVY
                continue

            if nextLineState == USPOKOJENI_NEZAJ:
                cols = re.compile("[\s]{2,}").split(line.strip())
                if len(cols) == 2:
                    self.model.Vysledek_rizeni.Predpoklad_uspokojeni_nezaj_vyse = self.priceValue(cols[0])
                    self.model.Vysledek_rizeni.Predpoklad_uspokojeni_nezaj_mira = self.priceValue(cols[1])
                    nextLineState = 0
            elif nextLineState == ZASLANI_VYZVY:
                cols = re.compile("[\s]{2,}").split(line.strip())
                if len(cols) == 1 and len(cols[0]) > 7:
                    self.model.Vysledek_rizeni.Zaslani_vyzvy_ukonceni_srazek = cols[0]
                break # konec tabulky

    def run(self):
        super().run()

        self._prubehRizeni()
        self._vysledekRizeni()
