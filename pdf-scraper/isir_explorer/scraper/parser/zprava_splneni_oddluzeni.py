from .model.zprava_splneni_oddluzeni import ZpravaSplneniOddluzeni
from .isir_parser import IsirParser
from .model.parts.osoba import *
from .model.parts.spisova_znacka import *
import re

class ZpravaSplneniOddluzeniParser(IsirParser):
    """Parser pro čtení formulářů typu Zpráva o splnění oddlužení.
    """

    #: :obj:`int` : 
    #: Verze scraperu tohoto typ dokumentu. Měla by být inkrementována při každé podstatné změně.
    VERZE_SCRAPER = 1

    def __init__(self, data):
        super().__init__(data)
        self.model = ZpravaSplneniOddluzeni()

    def extractDocument(self):
        doc_start = "^[\s]*A\. Průběh insolvenčního řízení"
        doc_end = "^[\s]*F\. Přílohy"
        self.extractDocumentByRange(doc_start, doc_end)

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
        
        # Textova pole pod tabulkou
        # Zprava o prubehu rizeni
        self.model.Vysledek_rizeni.Zprava_o_prubehu = self.textBlock(self.reTextBetween(
            txt,
            ".*míře plnění \(např. pracovní neschopnost, ztráta zaměstnání či neposkytování daru třetí osobou\):[\s]*$",
            "^[\s]*Insolvenční správce uvádí, že dlužník řádně plnil všechny povinnosti podle insolvenčního zákona a uložené rozhodnutím"
        ))

        # Doporuceni spravce
        self.model.Vysledek_rizeni.Doporuceni_spravce = self.textBlock(self.reTextBetween(
            txt,
            "^[\s]*Doporučení insolvenčního správce:",
            "^[\s]*Odůvodnění"
        ))

        # Oduvodneni doporuceni spravce
        self.model.Vysledek_rizeni.Doporuceni_spravce_oduvodneni = self.textBlock(self.reTextAfter(
            self.reTextAfter(txt, "^[\s]*Doporučení insolvenčního správce:", True),
            "^[\s]*Odůvodnění",
            True
        ))    

    def _vyuctovaniOdmenyIS(self):
        txt = self.reTextBetween(
            self.txt,
            "^[\s]*D\. Vyúčtování odměny a náhrady hotových výdajů insolvenčního správce",
            "^[\s]*E\. Detail vyúčtování odměny a náhrady nákladů insolvenčního správce"
        )

        lines = txt.split('\n')

        # Cisla stavu pro detekci hodnot nachazejicich se na jinych radkach, nez jejich nadpisy
        CELKOVA_ODMENA = 1
        HOTOVE_VYDAJE = 2

        nextLineState = 0
        for line in lines:
            if self.reMatch(line, '^[\s]*Celková odměna insolvenčního'):
                nextLineState = CELKOVA_ODMENA
                continue
            elif self.reMatch(line, '^[\s]*Hotové výdaje insolvenčního'):
                nextLineState = HOTOVE_VYDAJE
                continue
            elif self.reMatch(line, '^[\s]*výtěžku zpeněžení zajištěného'):
                nextLineState = 0
                row = self.reTextAfter(line, '^[\s]*výtěžku zpeněžení zajištěného')
                cols = re.compile("[\s]{2,}").split(row.strip())
                if len(cols) == 3:
                    # prvni sloupec je cena bez dph pokud je platce dph a je mozne jej ingorovat
                    cols = cols[1:]
                if len(cols) == 2:
                    self.model.Odmena_spravce.Vytezek_zpenezeni_zaji = self.priceValue(cols[0])
                    self.model.Odmena_spravce.Vytezek_zpenezeni_zaji_uhrazeno = self.priceValue(cols[1])
                continue
            elif self.reMatch(line, '^[\s]*výtěžku zpeněžení určeného k'):
                nextLineState = 0
                row = self.reTextAfter(line, '^[\s]*výtěžku zpeněžení určeného k')
                cols = re.compile("[\s]{2,}").split(row.strip())
                if len(cols) == 3:
                    # prvni sloupec je cena bez dph pokud je platce dph a je mozne jej ingorovat
                    cols = cols[1:]
                if len(cols) == 2:
                    self.model.Odmena_spravce.Vytezek_zpenezeni_rozdeleni = self.priceValue(cols[0])
                    self.model.Odmena_spravce.Vytezek_zpenezeni_rozdeleni_uhrazeno = self.priceValue(cols[1])
                break # Konec tabulky


            if nextLineState == CELKOVA_ODMENA:
                cols = re.compile("[\s]{2,}").split(line.strip())
                if len(cols) == 3:
                    # prvni sloupec je cena bez dph pokud je platce dph a je mozne jej ingorovat
                    cols = cols[1:]
                if len(cols) == 2:
                    self.model.Odmena_spravce.Celkova_odmena = self.priceValue(cols[0])
                    self.model.Odmena_spravce.Celkova_odmena_uhrazeno = self.priceValue(cols[1])
                    nextLineState = 0
            elif nextLineState == HOTOVE_VYDAJE:
                cols = re.compile("[\s]{2,}").split(line.strip())
                if len(cols) == 3:
                    # prvni sloupec je cena bez dph pokud je platce dph a je mozne jej ingorovat
                    cols = cols[1:]
                if len(cols) == 2:
                    self.model.Odmena_spravce.Hotove_vydaje = self.priceValue(cols[0])
                    self.model.Odmena_spravce.Hotove_vydaje_uhrazeno = self.priceValue(cols[1])
                    nextLineState = 0

        # Komentář IS k vyuctovani odmen
        txt = self.reTextAfter(
            self.txt,
            "^[\s]*I\. Odměna a hotové výdaje",
            True
        )
        self.model.Odmena_spravce.Zprava_spravce = self.textBlock(self.reTextAfter(txt, "^[\s]*Komentář:[\s]*$", True))

    def run(self):
        super().run()

        self._prubehRizeni()
        self._vysledekRizeni()
        self._vyuctovaniOdmenyIS()
