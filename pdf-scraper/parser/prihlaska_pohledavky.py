from parser.model.prihlaska_pohledavky import PrihlaskaPohledavky
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *


class PrihlaskaParser(IsirParser):

    def __init__(self, data):
        self.txt = data
        self.lines = data.split('\n')
        self.model = PrihlaskaPohledavky()
        super().__init__()

    def _soudSpisovaZnacka(self):
        for line in self.lines:
            if "Soud" in line and "Spis. značka" in line:
                soud = self.textBetween(line, "Soud", "Spis. značka")
                znackaTxt = self.removeSpaces(self.textAfter(line, "Spis. značka"))
                self.model.setSoud(soud, self.spisovaZnacka(znackaTxt))

    def _dluznik(self):
        txt = self.textBetween(self.txt, "     Dlužník", "     Věřitel")
        lines = txt.split('\n')
        dluznik = Dluznik()
        for line in lines:
            if "Příjmení:" in line and "Jméno:" in line:
                dluznik.Fyzicka_osoba.Udaje.Prijmeni = self.textBetween(line, "Příjmení:", "Jméno:")
                dluznik.Fyzicka_osoba.Udaje.Jmeno = self.textAfter(line, "Jméno:")
            elif "Rodné číslo:" in line:
                # bez lomitka
                dluznik.Fyzicka_osoba.Udaje.Rodne_cislo = self.numbersOnly(self.textAfter(line, "Rodné číslo:"))
        self.model.Dluznik = dluznik

    def _veritel(self):
        txt = self.textBetween(self.txt, "     Věřitel", "I vyplní se pouze u zahraničních osob")
        lines = txt.split('\n')
        veritel = Veritel()
        for line in lines:
            if "Název/obch.firma:" in line:
                veritel.Pravnicka_osoba.Udaje.Nazev = self.textAfter(line, "Název/obch.firma:")
            elif "IČ:" in line and "Jiné registr. č.:" in line:
                # RC bez lomitka
                veritel.Pravnicka_osoba.Udaje.IC = self.numbersOnly(self.textAfter(line, "Rodné číslo:"))
        self.model.Veritel = veritel

    def _pohledavky(self):
        txt = self.textBetween(self.txt, "Pohledávka č. 1", "54 Celková výše přihlášených pohledávek")
        lines = txt.split('\n')
        pohledavka = Pohledavka()
        for line in lines:
            if "Typ pohledávky:" in line:
                pohledavka.Typ = self.textAfter(line, "Typ pohledávky:")
            elif "Výše jistiny (Kč):" in line:
                pohledavka.Vyse_jistiny = self.priceValue(self.textAfter(line, "Výše jistiny (Kč):"))
            elif "Celková výše pohledávky:" in line:
                pohledavka.Celkova_vyse = self.priceValue(self.textAfter(line, "Celková výše pohledávky:"))

        pohledavka.Duvod_vzniku = self.textBlock(self.textBetween(txt, "06 Důvod vzniku:", "07 Vykonatelnost:"))
        pohledavka.Dalsi_okolnosti = self.textBlock(self.textAfter(txt, "10 Další okolnosti:"))

        self.model.Pohledavky.append(pohledavka)

    def run(self):
        # úvodní část soud a spis. značka řízení
        self._soudSpisovaZnacka()

        # informace o dlužníkovi
        self._dluznik()

        # informace o věřiteli
        self._veritel()

        # data pohledavek
        self._pohledavky()

        print(self.model.toJSON())
