from parser.model.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeni, ZaznamVykazuPlneni
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

    def _mesicniVykazPlneni(self):
        txt = self.reTextAfter(self.txt, "^[\s]*B\. MĚSÍČNÍ VÝKAZ PLNĚNÍ SPLÁTKOVÉHO KALENDÁŘE", True)
        lines = txt.split('\n')
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
        print(tabulkaPlneni)
        prijemMesicne = []

        for i in range(self.colsCount):
            mesic = ZaznamVykazuPlneni()
            mesic.Rok = self.numbersOnly(tabulkaPlneni["Rok"][i])
            mesic.Mesic = self.numbersOnly(tabulkaPlneni["Mesic"][i])
            mesic.Prijem = self.priceValue(tabulkaPlneni["Prijem"][i])
            mesic.Srazky = self.priceValue(tabulkaPlneni["Srazky"][i])
            mesic.ZMNNB = self.priceValue(tabulkaPlneni["ZMNNB"][i])
            mesic.Vyzivovane_osoby = self.numbersOnly(tabulkaPlneni["Vyzivovane_osoby"][i])
            mesic.Nepostizitelne = self.priceValue(tabulkaPlneni["Nepostizitelne"][i])
            mesic.Postizitelne = self.priceValue(tabulkaPlneni["Postizitelne"][i])
            mesic.Vraceno_dluznikum = self.priceValue(tabulkaPlneni["Vraceno_dluznikum"][i])
            mesic.Mimoradny_prijem = self.priceValue(tabulkaPlneni["Mimoradny_prijem"][i])
            mesic.Darovaci_smlouva = self.priceValue(tabulkaPlneni["Darovaci_smlouva"][i])
            mesic.K_prerozdeleni = self.priceValue(tabulkaPlneni["K_prerozdeleni"][i])
            mesic.Odmena_IS = self.priceValue(tabulkaPlneni["Odmena_IS"][i])
            mesic.Vyzivne = self.priceValue(tabulkaPlneni["Vyzivne"][i])
            mesic.Ostatnim_veritelum = self.priceValue(tabulkaPlneni["Ostatnim_veritelum"][i])
            prijemMesicne.append(mesic)
        self.model.VykazPlneni.Prijem = prijemMesicne

    def run(self):
        super().run()

        self._zpravaSpravcePlneni()

        self._mesicniVykazPlneni()

        #print(self.txt)