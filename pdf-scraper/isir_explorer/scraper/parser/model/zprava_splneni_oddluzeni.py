from .isir_dokument import IsirDokument

class PrubehRizeni:
    def __init__(self):
        self.Oddluzeni_povoleno = None
        self.Oddluzeni_schvaleno = None
        self.Zahajeno = None
        self.Zjisteni_upadku = None

class VysledekRizeni:
    def __init__(self):
        self.Posledni_splatka = None
        self.Zaslani_vyzvy_ukonceni_srazek = None
        self.Doporuceni_spravce = None
        self.Doporuceni_spravce_oduvodneni = None
        self.Zprava_o_prubehu = None
        self.Predpoklad_uspokojeni_nezaj_mira = None
        self.Predpoklad_uspokojeni_nezaj_vyse = None
        self.Uspokojeni_nezaj_mira = None
        self.Uspokojeni_nezaj_vyse = None
        self.Uspokojeni_zaj_mira = None
        self.Uspokojeni_zaj_vyse = None
        self.Preplatek = None

class OdmenaSpravce:
    def __init__(self):
        self.Celkova_odmena = None
        self.Celkova_odmena_uhrazeno = None
        self.Hotove_vydaje = None
        self.Hotove_vydaje_uhrazeno = None
        self.Vytezek_zpenezeni_rozdeleni = None
        self.Vytezek_zpenezeni_rozdeleni_uhrazeno = None
        self.Vytezek_zpenezeni_zaji = None
        self.Vytezek_zpenezeni_zaji_uhrazeno = None
        self.Zprava_spravce = None

class ZpravaSplneniOddluzeni(IsirDokument):

    TYP_DOKUMENTU = "ZpravaSplneniOddluzeni"

    def __init__(self):
        super().__init__()

        self.Prubeh_rizeni = PrubehRizeni()
        self.Vysledek_rizeni = VysledekRizeni()
        self.Odmena_spravce = OdmenaSpravce()
