from .model.prihlaska_pohledavky import PrihlaskaPohledavky
from .isir_parser import IsirParser
from .model.parts.osoba import *
from .model.parts.spisova_znacka import *
import re

class PrihlaskaParser(IsirParser):
    """Parser pro čtení formulářů typu Přihláška pohledávky.
    """

    def __init__(self, data):
        super().__init__(data)
        self.model = PrihlaskaPohledavky()

    def extractDocument(self):
        doc_start = "^[\s]{3,}PŘIHLÁŠKA POHLEDÁVKY[\s]*$"
        doc_end = "^[\s]*Způsob doručení přihlášky pohledávky na soud:"
        self.extractDocumentByRange(doc_start, doc_end)

    def removeVersionLine(self):
        """Prihlasky pohledavek neobsahuji strankovani
        """
        temp = []
        for line in self.lines:
            res = re.match('^[\s]{60,}Verze ([A-Za-z0-9\-]+)$', line)
            if res:
                # Ulozit verzi pokud jeste neni nastavena
                if self.model.Metadata.Verze is None:
                    self.model.Metadata.Verze = res[1]
            else:
                temp.append(line)
        self.lines = temp
        self.txt = '\n'.join(temp)

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
                udaje.Rodne_cislo = self.numbersOnly(self.textAfter(line, "Rodné číslo:"), toInt=False)
            elif "IČ:" in line and "Jiné registr. č.:" in line:
                udaje.IC = self.numbersOnly(self.textBetween(line, "IČ:", "Jiné registr. č.:"), toInt=False)
                udaje.Jine_reg_cislo = self.numbersOnly(self.textAfter(line, "Jiné registr. č.:"), toInt=False)
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
        txt = self.reTextBetween(self.txt, "^[\s]+Dlužník", "^[\s]+Věřitel")
        lines = txt.split('\n')
        udaje = self._udajeOsoby(lines)
        self.model.Dluznik = Dluznik(udaje)

    def _veritel(self):
        txt = self.reTextBetween(self.txt, "^[\s]+Věřitel", "^[\s]+I vyplní se pouze u zahraničních osob")
        lines = txt.split('\n')
        udaje = self._udajeOsoby(lines)
        self.model.Veritel = Veritel(udaje)

    def _vlastnostiPohledavky(self, txtVlastnosti, pohledavka):
        # Obsah teto sekce je aktualne ukladan pro analyzu formatu
        with open('data/vlastnosti/'+repr(self.model.Dluznik)+'_'+str(len(self.model.Pohledavky.Pohledavky)+1), 'w') as f:
            f.write(txtVlastnosti)

        STAV_ZPUSOB_PODRIZENI = 1
        STAV_CASTKA_PODRIZENI = 2
        STAV_SPLATNOST = 3
        stav = 0
        for line in txtVlastnosti.split('\n'):
            if stav == STAV_ZPUSOB_PODRIZENI:
                if "Ve výši (Kč)" in line:
                    stav = STAV_CASTKA_PODRIZENI
                    pohledavka.Vlastnosti.PodrizenaZpusob = self.textBlock(pohledavka.Vlastnosti.PodrizenaZpusob)
                    continue
                if hasattr(pohledavka.Vlastnosti, "PodrizenaZpusob"):
                    pohledavka.Vlastnosti.PodrizenaZpusob += line
                else:
                    pohledavka.Vlastnosti.PodrizenaZpusob = line
                continue
            elif stav == STAV_CASTKA_PODRIZENI:
                pohledavka.Vlastnosti.PodrizenaCastka = self.priceValue(line)
                stav = 0
                continue

            if "Splatná:" in line:
                splatna = "Splatná od:" in line
                pohledavka.Vlastnosti.Splatna = splatna
                if splatna:
                    stav = STAV_SPLATNOST
                    pohledavka.Vlastnosti.SplatnaOd = []
                    continue
            if "Podřízená:" in line:
                podrizena = "Způsob podřízení:" in line
                pohledavka.Vlastnosti.Podrizena = podrizena
                if podrizena:
                    stav = STAV_ZPUSOB_PODRIZENI
            # Konec sekce Vlastnosti pohledavky
            if "Pohledávka:" in line:
                break

            if stav == STAV_SPLATNOST:
                splatnaTxt = line.strip()
                columns = splatnaTxt.split('   ', 1)
                vCastce = None
                od = None
                if len(columns) == 1:
                    # pripad, kdy je vyplnen pouze jeden z udaju Splatna od: / V castce:
                    if self.reMatch(columns[0], "^([0-9]+ )*[0-9]+(,[0-9]+)?$"):
                        vCastce = self.priceValue(columns[0])
                    elif columns[0]!="":
                        od = columns[0]
                elif len(columns) == 2:
                    od = columns[0].strip()
                    vCastce = self.priceValue(columns[1])
                if vCastce is not None or od is not None:
                    splatnaOd = SplatnaOd()
                    splatnaOd.Od = od
                    splatnaOd.V_castce = vCastce
                    pohledavka.Vlastnosti.SplatnaOd.append(splatnaOd)

    def _pohledavka(self, txt):
        lines = txt.split('\n')
        pohledavka = Pohledavka()
        for line in lines:
            if self.reMatch(line, '^[\s]*Typ pohledávky:'):
                pohledavka.Typ = self.textAfter(line, "Typ pohledávky:")
            elif self.reMatch(line, '^[\s]*Výše jistiny \(Kč\):'):
                pohledavka.Vyse_jistiny = self.priceValue(self.textAfter(line, "Výše jistiny (Kč):"))
            elif self.reMatch(line, '^[\s]*Celková výše pohledávky:'):
                pohledavka.Celkova_vyse = self.priceValue(self.textAfter(line, "Celková výše pohledávky:"))

        pohledavka.Duvod_vzniku = self.textBlock(self.fieldText(txt, "^[\s]*[0-9]+ Důvod vzniku:"))
        pohledavka.Dalsi_okolnosti = self.textBlock(self.fieldText(txt, "^[\s]*[0-9]+ Další okolnosti:"))

        # Vykonatelnost
        txtVykonatelnost = self.fieldText(txt, "^[\s]*[0-9]+ Vykonatelnost:")
        for line in txtVykonatelnost.split('\n'):
            if "pro částku:" in line and "dle:" in line:
                pohledavka.Vykonatelnost = Vykonatelnost()
                pohledavka.Vykonatelnost.Pro_castku = self.priceValue(self.textBetween(line, "pro částku:", "dle:"))
                pohledavka.Vykonatelnost.Dle = self.textAfter(line, "dle:")

        # Prislusenstvi
        txtPrislusenstvi = self.fieldText(txt, "[\s]*[0-9]+ Příslušenství:")
        for line in txtPrislusenstvi.split('\n'):
            if self.reMatch(line, '^[\s]*Výše \(Kč\):'):
                pohledavka.Prislusenstvi = Prislusenstvi()
                pohledavka.Prislusenstvi.Vyse = self.priceValue(self.textAfter(line, "Výše (Kč):"))
                pohledavka.Prislusenstvi.Druh = self.textBlock(self.textBetween(txtPrislusenstvi, "Druh:", "Výše (Kč):"))
                pohledavka.Prislusenstvi.Zpusob_vypoctu = self.textBlock(self.fieldText(txtPrislusenstvi, "^[\s]*Způsob výpočtu:"))
                break

        # Vlastnosti (zatim faze sbirani dat)
        txtVlastnosti = self.fieldText(txt, "[\s]*[0-9]+ Vlastnosti pohledávky:")
        self._vlastnostiPohledavky(txtVlastnosti, pohledavka)

        return pohledavka

    def _pohledavky(self):
        pohledavkyText = re.compile('^[\s]*Pohledávka č\.[\s]+[0-9]+[\s]*$', re.MULTILINE).split(self.txt)

        if len(pohledavkyText) >= 2:
            pohledavkyText.pop(0) # Odstranit zacatek
        
        # posledni pohledavka
        posledni = pohledavkyText.pop()
        konec = self.reSplitText(posledni, '^[\s]*[0-9]+ Celková výše přihlášených pohledávek \(Kč\):.*', keep_split=True)
        pohledavkyText.append(konec[0]) # posledni pohledavka
        sumarizace = konec[1]

        for cislo, pohledavkaText in enumerate(pohledavkyText):
            pohledavka = self._pohledavka(pohledavkaText)
            pohledavka.Cislo = cislo+1
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
                break #konec sumarizace

    def run(self):
        super().run()

        # úvodní část soud a spis. značka řízení
        self._soudSpisovaZnacka()

        # informace o dlužníkovi
        self._dluznik()

        # informace o věřiteli
        self._veritel()

        # data pohledavek
        self._pohledavky()
