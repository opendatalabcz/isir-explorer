from parser.model.prihlaska_pohledavky import PrihlaskaPohledavky
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *
import re

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

    def _udajeOsoby(self, lines):
        udaje = UdajeOsoby()
        for line in lines:
            if "Příjmení:" in line and "Jméno:" in line:
                udaje.Prijmeni = self.textBetween(line, "Příjmení:", "Jméno:")
                udaje.Jmeno = self.textAfter(line, "Jméno:")
            elif "Titul za jm.:" in line and "Titul před jm.:" in line:
                udaje.Titul_za = self.textBetween(line, "Titul za jm.:", "Titul před jm.:")
                udaje.Titul_pred = self.textAfter(line, "Titul před jm.:")
            elif "Datum narození:" in line and "Rodné číslo:" in line:
                udaje.Datum_narozeni = re.sub(r"[^0-9.]", "", self.textBetween(line, "Datum narození:", "Rodné číslo:"))
                # RC bez lomitka
                udaje.Rodne_cislo = self.numbersOnly(self.textAfter(line, "Rodné číslo:"))
            elif "IČ:" in line and "Jiné registr. č.:" in line:
                udaje.IC = self.numbersOnly(self.textBetween(line, "IČ:", "Jiné registr. č.:"))
                udaje.Jine_reg_cislo = self.numbersOnly(self.textAfter(line, "Jiné registr. č.:"))
            elif "Název/obch.firma:" in line:
                udaje.Nazev = self.textAfter(line, "Název/obch.firma:")
            elif "Ulice:" in line:
                udaje.Sidlo.Ulice = self.textAfter(line, "Ulice:")
            elif "Č.p./č.e.:" in line and "Č.o.:" in line:
                udaje.Sidlo.Cp = self.textBetween(line, "Č.p./č.e.:", "Č.o.:")
                udaje.Sidlo.Co = self.textAfter(line, "Č.o.:")
            elif "Obec:" in line:
                udaje.Sidlo.Obec = self.textAfter(line, "Obec:")
            elif "PSČ:" in line and "Část obce:" in line:
                udaje.Sidlo.PSC = self.textBetween(line, "PSČ:", "Část obce:")
                udaje.Sidlo.Cast_obce = self.textAfter(line, "Část obce:")
            elif "Stát:" in line:
                udaje.Sidlo.Stat = self.textAfter(line, "Stát:")
            elif "Číslo účtu:" in line:
                udaje.Cislo_uctu = self.textAfter(line, "Číslo účtu:")

        return udaje

    def _dluznik(self):
        txt = self.textBetween(self.txt, "     Dlužník", "     Věřitel")
        lines = txt.split('\n')
        udaje = self._udajeOsoby(lines)
        self.model.Dluznik = Dluznik(udaje)

    def _veritel(self):
        txt = self.textBetween(self.txt, "     Věřitel", "I vyplní se pouze u zahraničních osob")
        lines = txt.split('\n')
        udaje = self._udajeOsoby(lines)
        self.model.Veritel = Veritel(udaje)

    def _pohledavka(self, txt):
        lines = txt.split('\n')
        pohledavka = Pohledavka()
        for line in lines:
            if "Typ pohledávky:" in line:
                pohledavka.Typ = self.textAfter(line, "Typ pohledávky:")
            elif "Výše jistiny (Kč):" in line:
                pohledavka.Vyse_jistiny = self.priceValue(self.textAfter(line, "Výše jistiny (Kč):"))
            elif "Celková výše pohledávky:" in line:
                pohledavka.Celkova_vyse = self.priceValue(self.textAfter(line, "Celková výše pohledávky:"))

        #pohledavka.Duvod_vzniku = self.textBlock(self.textBetween(txt, "06 Důvod vzniku:", "07 Vykonatelnost:"))
        #pohledavka.Dalsi_okolnosti = self.textBlock(self.textAfter(txt, "10 Další okolnosti:"))
        return pohledavka

    def _pohledavky(self):
        pohledavkyText = re.compile('^[\s]*Pohledávka č\.[\s]+[0-9]+[\s]*$', re.MULTILINE).split(self.txt)

        if len(pohledavkyText) >= 2:
            pohledavkyText.pop(0) # Odstranit zacatek
        
        # posledni pohledavka
        posledni = pohledavkyText.pop()
        konec = self.reSplitText(posledni, '(^[\s]*[0-9]+ Celková výše přihlášených pohledávek \(Kč\):.*)', keepSplit=True)
        pohledavkyText.append(konec[0]) # posledni pohledavka
        sumarizace = konec[1]

        for pohledavkaText in pohledavkyText:
            pohledavka = self._pohledavka(pohledavkaText)
            self.model.Pohledavky.Pohledavky.append(pohledavka)

        sumLines = sumarizace.split('\n')
        for line in sumLines:
            if self.reMatch(line, '^[\s]*[0-9]+ Celková výše přihlášených pohledávek \(Kč\):'):
                self.model.Pohledavky.Celkova_vyse = self.priceValue(self.reTextAfter(line, '^[\s]*[0-9]+ Celková výše přihlášených pohledávek \(Kč\):'))
            elif self.reMatch(line, '^[\s]*[0-9]+ Celková výše nezajištěných pohledávek \(Kč\):'):
                self.model.Pohledavky.Celkova_vyse_nezajistenych = self.priceValue(self.reTextAfter(line, '^[\s]*[0-9]+ Celková výše nezajištěných pohledávek \(Kč\):'))
            elif self.reMatch(line, '^[\s]*[0-9]+ Celková výše zajištěných pohledávek \(Kč\):'):
                self.model.Pohledavky.Celkova_vyse_zajistenych = self.priceValue(self.reTextAfter(line, '^[\s]*[0-9]+ Celková výše zajištěných pohledávek \(Kč\):'))
            elif self.reMatch(line, '^[\s]*[0-9]+ Počet pohledávek:'):
                self.model.Pohledavky.Pocet_pohledavek = self.numbersOnly(self.reTextAfter(line, '^[\s]*[0-9]+ Počet pohledávek:'))
            elif self.reMatch(line, '^[\s]*[0-9]+ Počet vložených stran:'):
                self.model.Pohledavky.Pocet_vlozenych_stran = self.numbersOnly(self.reTextAfter(line, '^[\s]*[0-9]+ Počet vložených stran:'))
                break

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
