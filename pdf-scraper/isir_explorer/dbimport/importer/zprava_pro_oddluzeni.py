from .isir_importer import IsirImporter


class ZpravaProOddluzeniImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Zpráva pro oddlužení.
    """

    TYP_DOKUMENTU = 3

    #: :obj:`dict` : 
    #: Číselník stavů typu majetku v soupisu majetku
    SOUPIS_MAJETKU = {
        "Financni_prostredky": 1,
        "Movity": 2,
        "Nemovity": 3,
        "Ostatni": 4,
        "Pohledavky": 5,
    }

    #: :obj:`dict` : 
    #: Číselník kategorií předpokládané míry uspokojení věřitelů
    TYP_MIRY_USPOKOJENI = {
        "Splat_kal_zpen_maj": 1,
        "Splatkovy_kalendar": 2,
        "Zpenezeni_majetku": 3,
    }

    def __init__(self, db, document):
        super().__init__(db, document)

        self.zpravaId = None

    def _typVeriteleDistribSchematu(self, jeZajisteny, zpravaId, schema):
        res = []
        for veritel in schema:
            res.append({
                'zpro_id': zpravaId,
                'typ': jeZajisteny,
                'veritel': veritel["Veritel"],
                'castka': veritel["Castka"],
                'podil': veritel["Podil"],
            })
        return res

    def _typVeriteleMiraUspokojeni(self, jeZajisteny, zpravaId, predpokladUspokojeni):
        if not predpokladUspokojeni:
            return []
        
        res = []
        for key in self.TYP_MIRY_USPOKOJENI:
            if key not in predpokladUspokojeni:
                continue
            cisloTypuUspokojeni = self.TYP_MIRY_USPOKOJENI[key]
            predpoklad = {
                "zpro_id": zpravaId,
                "typ": jeZajisteny,
                "uspokojeni": cisloTypuUspokojeni,
                "mira": predpokladUspokojeni[key]["Mira"],
                "vyse": predpokladUspokojeni[key]["Vyse"],
            }

            # Vkladat jen nenulove radky
            if predpoklad["mira"] or predpoklad["vyse"]:
                res.append(predpoklad)
        return res

    async def zpravaProOddluzeni(self, dokumentId):
        self.zpravaId = await self.insert("zprava_pro_oddluzeni",{
            "id": dokumentId,
            "odmena_za_sepsani_navrhu": 
                self.doc["Hospodarska_situace"]["Odmena_za_sepsani_navrhu"],
            "povinnen_vydat_obydli":
                self.doc["Hospodarska_situace"]["Povinnen_vydat_obydli"],
            "vyse_zalohy":
                self.doc["Hospodarska_situace"]["Vyse_zalohy"],
            "vytezek_zpenezeni_obydli":
                self.doc["Hospodarska_situace"]["Vytezek_zpenezeni_obydli"],
            "zpracovatel_navrhu":
                self.doc["Hospodarska_situace"]["Zpracovatel_navrhu"],

            "prijmy_celkem":
                self.doc["Prijmy_dluznika"]["Celkem"],
            "prijmy_komentar":
                self.doc["Prijmy_dluznika"]["Komentar"],

            "celkem_majetek_oceneni":
                self.doc["Soupis_majetku"]["Celkem"]["Oceneni"],
            "celkem_majetek_nezajisteno":
                self.doc["Soupis_majetku"]["Celkem"]["Nezajisteno"],
            "celkem_majetek_zajisteno":
                self.doc["Soupis_majetku"]["Celkem"]["Zajisteno"],

            "okolnosti_proti_oddluzeni":
                self.doc["Okolnosti_proti_oddluzeni"],
            "navrh_dluznika":
                self.doc["Navrh_dluznika"],
            "navrh_spravce":
                self.doc["Navrh_spravce"],
        })

    async def soupisMajetku(self):
        soupis = []
        for key in self.SOUPIS_MAJETKU:
            if key not in self.doc["Soupis_majetku"]:
                continue
            cisloTypyMajetku = self.SOUPIS_MAJETKU[key]
            typMajetku = {
                "zpro_id": self.zpravaId,
                "typ_majetku": cisloTypyMajetku,
                "oceneni": self.doc["Soupis_majetku"][key]["Oceneni"],
                "nezajisteno": self.doc["Soupis_majetku"][key]["Nezajisteno"],
                "zajisteno": self.doc["Soupis_majetku"][key]["Zajisteno"],
            }

            # Vkladat jen nenulove radky
            if typMajetku["oceneni"] or typMajetku["nezajisteno"] or typMajetku["zajisteno"]:
                soupis.append(typMajetku)
        
        await self.insertMany("zpro_soupis_majetku", soupis)

    async def prijemDluznika(self):
        prijmy = []
        for prijem in self.doc["Prijmy_dluznika"]["Prijmy"]:
            prijmy.append({
                "zpro_id": self.zpravaId,
                "nazev_platce": prijem["Nazev_platce"],
                "adresa": prijem["Adresa"],
                "ico": prijem["ICO"],
                "typ": prijem["Typ"],
                "vyse": prijem["Vyse"],
            })
        await self.insertMany("zpro_prijem_dluznika", prijmy)

    async def distribucniSchema(self):
        dsNezajistene = self._typVeriteleDistribSchematu(False, self.zpravaId, self.doc["Distribucni_schema"]["Nezajistene"])
        dsZajistene   = self._typVeriteleDistribSchematu(True,  self.zpravaId, self.doc["Distribucni_schema"]["Zajistene"])
        distribucniSchema = dsNezajistene + dsZajistene
        await self.insertMany("zpro_distribucni_schema", distribucniSchema)

    async def predpokladUspokojeni(self):
        puNezajistene = self._typVeriteleMiraUspokojeni(False, self.zpravaId, self.doc["Predpoklad_uspokojeni"]["Nezajistene"])
        puZajistene = self._typVeriteleMiraUspokojeni(True, self.zpravaId, self.doc["Predpoklad_uspokojeni"]["Zajistene"])
        predpokladUspokojeni = puNezajistene + puZajistene
        await self.insertMany("zpro_predpoklad_uspokojeni", predpokladUspokojeni)

    async def importDocument(self, dokumentId):

        await self.zpravaProOddluzeni(dokumentId)

        # Soupis majetku
        await self.soupisMajetku()

        # Prijem dluznika
        await self.prijemDluznika()
        
        # Distribucni schema
        await self.distribucniSchema()

        # Predpoklad uspokojeni
        await self.predpokladUspokojeni()
