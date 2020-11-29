from .isir_importer import IsirImporter


class ZpravaSplneniOddluzeniImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Zpráva o splnění oddlužení.
    """

    def __init__(self, db, document):
        super().__init__(db, document)

        self.zpravaId = None

    async def zpravaPlneniOddluzeni(self):
        self.zpravaId = await self.insert("zprava_splneni_oddluzeni",{
            "oddluzeni_povoleno": 
                self.dateFormat(self.doc["Prubeh_rizeni"]["Oddluzeni_povoleno"]),
            "oddluzeni_schvaleno":
                self.dateFormat(self.doc["Prubeh_rizeni"]["Oddluzeni_schvaleno"]),
            "zahajeno":
                self.dateFormat(self.doc["Prubeh_rizeni"]["Zahajeno"]),
            "zjisteni_upadku":
                self.dateFormat(self.doc["Prubeh_rizeni"]["Zjisteni_upadku"]),
            "posledni_splatka":
                self.dateFormat(self.doc["Vysledek_rizeni"]["Posledni_splatka"]),
            "zaslani_vyzvy_ukonceni_srazek": 
                self.dateFormat(self.doc["Vysledek_rizeni"]["Zaslani_vyzvy_ukonceni_srazek"]),
            "doporuceni_spravce":
                self.doc["Vysledek_rizeni"]["Doporuceni_spravce"],
            "doporuceni_spravce_oduvodneni":
                self.doc["Vysledek_rizeni"]["Doporuceni_spravce_oduvodneni"],
            "zprava_o_prubehu":
                self.doc["Vysledek_rizeni"]["Zprava_o_prubehu"],
            "n_predpoklad_uspokojeni_mira":
                self.doc["Vysledek_rizeni"]["Predpoklad_uspokojeni_nezaj_mira"],
            "n_predpoklad_uspokojeni_vyse": 
                self.doc["Vysledek_rizeni"]["Predpoklad_uspokojeni_nezaj_vyse"],
            "n_uspokojeni_mira":
                self.doc["Vysledek_rizeni"]["Uspokojeni_nezaj_mira"],
            "n_uspokojeni_vyse":
                self.doc["Vysledek_rizeni"]["Uspokojeni_nezaj_vyse"],
            "z_uspokojeni_mira":
                self.doc["Vysledek_rizeni"]["Uspokojeni_zaj_mira"],
            "z_uspokojeni_vyse":
                self.doc["Vysledek_rizeni"]["Uspokojeni_zaj_vyse"],
            "preplatek": 
                self.doc["Vysledek_rizeni"]["Preplatek"],
        })

    async def odmenaSpravce(self):
        await self.insert("zspo_odmena_spravce",{
            "zspo_id":
                self.zpravaId,
            "celkova_odmena": 
                self.doc["Odmena_spravce"]["Celkova_odmena"],
            "celkova_odmena_uhrazeno":
                self.doc["Odmena_spravce"]["Celkova_odmena_uhrazeno"],
            "hotove_vydaje":
                self.doc["Odmena_spravce"]["Hotove_vydaje"],
            "hotove_vydaje_uhrazeno":
                self.doc["Odmena_spravce"]["Hotove_vydaje_uhrazeno"],
            "vytezek_zpenezeni_rozdeleni":
                self.doc["Odmena_spravce"]["Vytezek_zpenezeni_rozdeleni"],
            "vytezek_zpenezeni_rozdeleni_uhrazeno": 
                self.doc["Odmena_spravce"]["Vytezek_zpenezeni_rozdeleni_uhrazeno"],
            "vytezek_zpenezeni_zaji":
                self.doc["Odmena_spravce"]["Vytezek_zpenezeni_zaji"],
            "vytezek_zpenezeni_zaji_uhrazeno":
                self.doc["Odmena_spravce"]["Vytezek_zpenezeni_zaji_uhrazeno"],
            "zprava_spravce":
                self.doc["Odmena_spravce"]["Zprava_spravce"],
        })

    async def importDocument(self):

        await self.zpravaPlneniOddluzeni()

        await self.odmenaSpravce()
