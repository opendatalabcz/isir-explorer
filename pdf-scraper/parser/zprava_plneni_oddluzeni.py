from parser.model.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeni, ZaznamVykazuPlneni, ZaznamUspokojeniVeritele
from parser.isir_parser import IsirParser
from parser.model.parts.osoba import *
from parser.model.parts.spisova_znacka import *
import re

class ZpravaPlneniOddluzeniParser(IsirParser):

    def __init__(self, data):
        self.txt = data
        self.lines = data.split('\n')
        self.model = ZpravaPlneniOddluzeni()

        # Pocet sloupcu v tabulce plneni splatkoveho kalendare (tj. pocet mesicu)
        self.colsCount = 0

        super().__init__()

    def extractDocument(self):
        self.txt = self.reTextBetween(self.txt, "^[\s]*A\. ZPRÁVA INSOLVENČNÍHO SPRÁVCE O PLNĚNÍ POVINNOSTÍ DLUŽNÍKA V ODDLUŽENÍ", "^[\s]*C\. Přílohy")
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

    def _zpravaSpravcePlneni(self):
        txt = self.reTextBefore(self.txt, "^[\s]*B\. MĚSÍČNÍ VÝKAZ PLNĚNÍ SPLÁTKOVÉHO KALENDÁŘE", True)
        self.model.ZpravaSpravce.Plni_povinnosti = self.reLineTextAfter(txt, "^[\s]*Dlužník plní povinnosti v rámci schváleného způsobu oddlužení")
        self.model.ZpravaSpravce.Duvod_neplneni = self.textBlock(self.reTextBetween(txt, "^[\s]*-[\s]*důvod neplnění schváleného způsobu oddlužení:", "^[\s]*-[\s]*stanovisko dlužníka, jak se hodlá vypořádat se vzniklou situací:"))
        self.model.ZpravaSpravce.Stanovisko_dluznika = self.textBlock(self.reTextBetween(txt, "^[\s]*-[\s]*stanovisko dlužníka, jak se hodlá vypořádat se vzniklou situací:", "^[\s]*Vyjádření insolvenčního správce k plnění povinností dlužníka v oddlužení:"))
        self.model.ZpravaSpravce.Vyjadreni_spravce = self.textBlock(self.reTextBetween(txt, "^[\s]*Vyjádření insolvenčního správce k plnění povinností dlužníka v oddlužení:", "^[\s]*Aktuální míra uspokojení nezajištěných věřitelů"))

        self.model.ZpravaSpravce.Mira_uspokojeni.Nezajistene_aktualni = self.priceValue(self.reLineTextAfter(txt, "^[\s]*Aktuální míra uspokojení nezajištěných věřitelů"))
        self.model.ZpravaSpravce.Mira_uspokojeni.Nezajistene_ocekavana = self.priceValue(self.reLineTextAfter(txt, "^[\s]*Očekávaná míra uspokojení nezajištěných věřitelů"))
        #TODO zajisteni veritele (?)
        
        txt = self.reTextAfter(txt, "^[\s]*Doporučení insolvenčního správce:", True)
        self.model.ZpravaSpravce.Doporuceni_spravce = self.textBlock(self.reTextBetween(txt, "^[\s]*Doporučení insolvenčního správce:", "^[\s]*Odůvodnění:"))
        self.model.ZpravaSpravce.Doporuceni_spravce_oduvodneni = self.textBlock(self.reTextAfter(txt, "^[\s]*Odůvodnění:", True))
    
    def _sloupceVykazuPlneni(self, line, reg, checkColsCount=True):
        colsTxt = self.reLineTextAfter(line, reg)
        cols = re.compile("[\s]{2,}").split(colsTxt.strip())
        if checkColsCount and len(cols) != self.colsCount:
            return None
        return cols

    def _mesicniVykazPlneniPrijmyDluznika(self, txt, lines):
        tabulkaPlneni = {}
        nextLine = None
        for line in lines:
            matched = True
            if self.reMatch(line, "^[\s]*Rok "):
                tabulkaPlneni["Rok"] = self._sloupceVykazuPlneni(line, "^[\s]*Rok ", False)
                self.colsCount = len(tabulkaPlneni["Rok"])
            elif self.reMatch(line, "^[\s]*Měsíc "):
                tabulkaPlneni["Mesic"] = self._sloupceVykazuPlneni(line, "^[\s]*Měsíc ")
            elif self.reMatch(line, "^[\s]*Příjem "):
                tabulkaPlneni["Prijem"] = self._sloupceVykazuPlneni(line, "^[\s]*Příjem ")
            elif self.reMatch(line, "^[\s]*Provedené srážky "):
                tabulkaPlneni["Srazky"] = self._sloupceVykazuPlneni(line, "^[\s]*Provedené srážky ")
            elif self.reMatch(line, "^[\s]*ZM\+NNB "):
                tabulkaPlneni["ZMNNB"] = self._sloupceVykazuPlneni(line, "^[\s]*ZM\+NNB ")
            elif self.reMatch(line, "^[\s]*Vyživované osoby "):
                tabulkaPlneni["Vyzivovane_osoby"] = self._sloupceVykazuPlneni(line, "^[\s]*Vyživované osoby ")
            elif self.reMatch(line, "^[\s]*Nepostižitelné "):
                tabulkaPlneni["Nepostizitelne"] = self._sloupceVykazuPlneni(line, "^[\s]*Nepostižitelné ")
            elif self.reMatch(line, "^[\s]*Postižitelné "):
                tabulkaPlneni["Postizitelne"] = self._sloupceVykazuPlneni(line, "^[\s]*Postižitelné ")
            elif self.reMatch(line, "^[\s]*Vráceno dlužníkům "):
                tabulkaPlneni["Vraceno_dluznikum"] = self._sloupceVykazuPlneni(line, "^[\s]*Vráceno dlužníkům ")
            elif self.reMatch(line, "^[\s]*Mimořádný příjem "):
                tabulkaPlneni["Mimoradny_prijem"] = self._sloupceVykazuPlneni(line, "^[\s]*Mimořádný příjem ")
            elif self.reMatch(line, "^[\s]*Darovací smlouva "):
                tabulkaPlneni["Darovaci_smlouva"] = self._sloupceVykazuPlneni(line, "^[\s]*Darovací smlouva ")
            elif self.reMatch(line, "^[\s]*K přerozdělení "):
                tabulkaPlneni["K_prerozdeleni"] = self._sloupceVykazuPlneni(line, "^[\s]*K přerozdělení ")
            elif self.reMatch(line, "^[\s]*- na odměnu IS "):
                tabulkaPlneni["Odmena_IS"] = self._sloupceVykazuPlneni(line, "^[\s]*- na odměnu IS ")
            elif self.reMatch(line, "^[\s]*- na výživné "):
                tabulkaPlneni["Vyzivne"] = self._sloupceVykazuPlneni(line, "^[\s]*- na výživné ")
            elif self.reMatch(line, "^[\s]*- ostatním věřitelům "):
                tabulkaPlneni["Ostatnim_veritelum"] = self._sloupceVykazuPlneni(line, "^[\s]*- ostatním věřitelům ")
                # Konec tabulky
                break
            elif self.reMatch(line, "^[\s]*- na jiné zapodstatové(?: pohledávky)? "):
                # Nadpis v tabulce je na dva radky, hodnoty precist z dalsi iterace
                cols = self._sloupceVykazuPlneni(line, "^[\s]*- na jiné zapodstatové(?: pohledávky)? ")
                if cols is not None:
                    tabulkaPlneni["Jine"] = cols
                else:
                    nextLine = "Jine"
                    matched = False
            elif nextLine:
                cols = self._sloupceVykazuPlneni(line, "^[\s]*")
                if cols:
                    tabulkaPlneni[nextLine] = cols
                else:
                    matched = False

            if matched:
                nextLine = None
        prijemMesicne = []

        NUMBERS_ONLY_COLUMNS = ["Rok", "Mesic", "Vyzivovane_osoby"]
        PRICE_COLUMNS = ["Prijem", "Srazky", "ZMNNB", "Nepostizitelne", "Postizitelne", "Vraceno_dluznikum",
            "Mimoradny_prijem", "Darovaci_smlouva", "K_prerozdeleni", "Odmena_IS", "Vyzivne", "Ostatnim_veritelum"]

        for i in range(self.colsCount):
            mesic = ZaznamVykazuPlneni()

            for key in NUMBERS_ONLY_COLUMNS:
                try:
                    val = self.numbersOnly(tabulkaPlneni[key][i])
                except KeyError:
                    val = None
                setattr(mesic, key, val)

            for key in PRICE_COLUMNS:
                try:
                    val = self.priceValue(tabulkaPlneni[key][i])
                except KeyError:
                    val = None
                setattr(mesic, key, val)

            prijemMesicne.append(mesic)
        self.model.VykazPlneni.Prijem = prijemMesicne

    class Zaznam:
        def __init__(self):
            self.Veritel = []
            self.Sloupce = []

    def _sloupcePrerozdeleniVeritelum(self, colsTxt):
        cols = re.compile("[\s]{2,}").split(colsTxt.strip())

        # pocet mesicu ve vykazu + sloupec podilu + sloupec castky
        if len(cols) != self.colsCount+2:
            return None
        return cols

    def _mesicniVykazPlneniPrerozdeleniVeritelum(self, txt, lines):
        
        obsahVykazu = False
        zaznamy = []
        zaznam = self.Zaznam()
        stav = 0 # 0=nic neprebyva, cte se novy zaznam, 1=zustatek nazvu veritele, 2=precten datovy radek s cisly ve stavu 1
        for i,line in enumerate(lines):
            if self.reMatch(line, "^.*Zjištěná pohledávka[\s]+Vyplaceno věřitelům"):
                obsahVykazu = True
                continue
            elif not obsahVykazu:
                continue
            
            # Rozdelit radek dle procentni hodnoty podilu (prvni z ciselnych sloupcu)
            parts = self.reSplitText(line, "([0-9]+(?:,[0-9]+)?[\s]?%)")
            if len(parts) == 2:

                if stav == 2:
                    zaznamy.append(zaznam)
                    zaznam = self.Zaznam()
                    stav = 0

                # Radek obsahuje ciselne hodnoty ve sloupcich (a mozna i nazev veritele)
                zaznam.Veritel.append(parts[0].strip())
                zaznam.Sloupce = self._sloupcePrerozdeleniVeritelum(parts[1].strip())

                if stav == 0:
                    zaznamy.append(zaznam)
                    zaznam = self.Zaznam()
                elif stav == 1:
                    stav = 2
            else:
                # Prazdny radek nebo radek s pokracujicim nazvem veritele
                text = parts[0].strip()
                if '' != text:
                    zaznam.Veritel.append(text)

                    if stav == 0:
                        stav = 1
                    elif stav == 2:
                        stav = 0
                        zaznamy.append(zaznam)
                        zaznam = self.Zaznam()

            # Konec části s rozpisem věřitelů, začátek řádků se sumarizací
            if self.reMatch(line, "^[\s]+Celkem přerozděleno"):
                lines = lines[i:]
                break
        print(zaznamy)

        for zaznam in zaznamy:
            vyplacenoVeriteli = ZaznamUspokojeniVeritele()
            vyplacenoVeriteli.Veritel = ' '.join(zaznam.Veritel)
            vyplacenoVeriteli.Podil = self.priceValue(zaznam.Sloupce[0])
            vyplacenoVeriteli.Castka = self.priceValue(zaznam.Sloupce[1])
            zaznam.Sloupce = zaznam.Sloupce[2:]
            for sloupec in zaznam.Sloupce:
                vyplacenoVeriteli.Vyplaceno.append(self.priceValue(sloupec))
            self.model.VykazPlneni.Rozdeleni.append(vyplacenoVeriteli)


    def _mesicniVykazPlneni(self):
        txt = self.reTextAfter(self.txt, "^[\s]*B\. MĚSÍČNÍ VÝKAZ PLNĚNÍ SPLÁTKOVÉHO KALENDÁŘE", True)
        lines = txt.split('\n')

        self._mesicniVykazPlneniPrijmyDluznika(txt, lines)

        self._mesicniVykazPlneniPrerozdeleniVeritelum(txt, lines)

    def run(self):
        super().run()

        self._zpravaSpravcePlneni()

        self._mesicniVykazPlneni()

        #print(self.txt)