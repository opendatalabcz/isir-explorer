from .isir_importer import IsirImporter


class ZpravaPlneniOddluzeniImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Zpráva o plnění oddlužení.
    """

    TYP_DOKUMENTU = 4

    def __init__(self, db, document):
        super().__init__(db, document)

        self.zpravaId = None

    async def zpravaPlneniOddluzeni(self, dokumentId):

        try:
            n_uspokojeni_ocekavana = self.doc["ZpravaSpravce"]["Mira_uspokojeni"]["Nezajistene_ocekavana"]
            n_uspokojeni_aktualni = self.doc["ZpravaSpravce"]["Mira_uspokojeni"]["Nezajistene_aktualni"]
        except KeyError:
            n_uspokojeni_ocekavana = None
            n_uspokojeni_aktualni = None

        try:
            z_uspokojeni_ocekavana = self.doc["ZpravaSpravce"]["Mira_uspokojeni"]["Zajistene_ocekavana"]
            z_uspokojeni_aktualni = self.doc["ZpravaSpravce"]["Mira_uspokojeni"]["Zajistene_aktualni"]
        except KeyError:
            z_uspokojeni_ocekavana = None
            z_uspokojeni_aktualni = None

        self.zpravaId = await self.insert("zprava_plneni_oddluzeni", {
            "id": dokumentId,
            "doporuceni_spravce":
                self.doc["ZpravaSpravce"]["Doporuceni_spravce"],
            "doporuceni_spravce_oduvodneni":
                self.doc["ZpravaSpravce"]["Doporuceni_spravce_oduvodneni"],
            "duvod_neplneni":
                self.doc["ZpravaSpravce"]["Duvod_neplneni"],
            "plni_povinnosti":
                self.doc["ZpravaSpravce"]["Plni_povinnosti"],
            "stanovisko_dluznika":
                self.doc["ZpravaSpravce"]["Stanovisko_dluznika"],
            "vyjadreni_spravce":
                self.doc["ZpravaSpravce"]["Vyjadreni_spravce"],
            "n_uspokojeni_ocekavana":
                n_uspokojeni_ocekavana,
            "n_uspokojeni_aktualni":
                n_uspokojeni_aktualni,
            "z_uspokojeni_ocekavana":
                z_uspokojeni_ocekavana,
            "z_uspokojeni_aktualni":
                z_uspokojeni_aktualni,
        })

    async def vykazPlneni(self):
        vykazPlneni = []
        for mesic in self.doc["VykazPlneni"]["Mesic"]:
            vykazPlneni.append({
                'zplo_id': self.zpravaId,
                'rok': mesic["Rok"],
                'mesic': mesic["Mesic"],
                'mesic_oddluzeni': mesic["Mesic_oddluzeni"],
                'prijem': mesic["Prijem"],
                'srazky': mesic["Srazky"],
                'zm_nnb': mesic["ZMNNB"],

                'vyzivovane_osoby': mesic["Vyzivovane_osoby"],
                'nepostizitelne': mesic["Nepostizitelne"],
                'postizitelne': mesic["Postizitelne"],
                'vraceno_dluznikum': mesic["Vraceno_dluznikum"],
                'mimoradny_prijem': mesic["Mimoradny_prijem"],
                'darovaci_smlouva': mesic["Darovaci_smlouva"],
                'k_prerozdeleni': mesic["K_prerozdeleni"],
                'odmena_is': mesic["Odmena_IS"],
                'vyzivne': mesic["Vyzivne"],
                'ostatnim_veritelum': mesic["Ostatnim_veritelum"],

                'celkem_prerozdeleno': mesic["Celkem_prerozdeleno"],
                'mira_uspokojeni': mesic["Mira_uspokojeni"],
                'mira_uspkojeni_ocekavana': mesic["Mira_uspkojeni_ocekavana"],
            })

        await self.insertMany("zplo_vykaz_plneni", vykazPlneni)

    async def vykazPrerozdeleni(self):
        vykazPrerozdeleni = []

        for veritel in self.doc["VykazPlneni"]["Rozdeleni"]:
            veritelId = await self.insert("zplo_vykaz_prerozdeleni_veritel", {
                "zplo_id": self.zpravaId,
                "veritel": veritel["Veritel"],
                "castka": veritel["Castka"],
                "podil": veritel["Podil"],
            })
            veritel["Id"] = veritelId

        for veritel in self.doc["VykazPlneni"]["Rozdeleni"]:

            # Kontrola asociace k jednotlivym mesicum vykazu Plneni
            if len(self.doc["VykazPlneni"]["Mesic"]) != len(veritel["Vyplaceno"]):
                continue

            for i, castka in enumerate(veritel["Vyplaceno"]):
                mesic = self.doc["VykazPlneni"]["Mesic"][i]["Mesic"]
                mesic_oddluzeni = self.doc["VykazPlneni"]["Mesic"][i]["Mesic_oddluzeni"]

                # Neukladat zaznam vykazu, pokud ve formulari neni uveden mesic, ke kteremu zaznam nalezi
                if not mesic or not mesic_oddluzeni:
                    continue

                vykazPrerozdeleni.append({
                    "zplo_veritel_id": veritel["Id"],
                    "rok": self.doc["VykazPlneni"]["Mesic"][i]["Rok"],
                    "mesic": mesic,
                    "mesic_oddluzeni": mesic_oddluzeni,
                    "vyplaceno": castka,
                })

        await self.insertMany("zplo_vykaz_prerozdeleni", vykazPrerozdeleni)

    async def importDocument(self, dokumentId):

        await self.zpravaPlneniOddluzeni(dokumentId)

        # Vykaz plneni
        await self.vykazPlneni()

        # Vykaz prerozdeleni veritelum
        await self.vykazPrerozdeleni()
