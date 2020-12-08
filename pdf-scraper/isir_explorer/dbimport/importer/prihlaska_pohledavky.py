from .isir_importer import IsirImporter


class PrihlaskaImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Přihláška pohledávky.
    """

    TYP_DOKUMENTU = 1

    TYP_POHLEDAVKY = {
        "nezajištěná - jednotlivě": 1,
        "nezajištěná - hromadně": 2,
    }

    def typPohledavky(self, typ):
        try:
            return self.TYP_POHLEDAVKY[typ]
        except KeyError:
            return None

    async def importDocument(self, dokumentId):

        # Pocet pohledavek nekdy neni vyplnen
        if self.doc["Pohledavky"]["Pocet_pohledavek"] is None:
            self.doc["Pohledavky"]["Pocet_pohledavek"] = len(self.doc["Pohledavky"]["Pohledavky"])

        prihlaskaId = await self.insert("prihlaska_pohledavky",{
            "id":
                dokumentId,
            "pocet_pohledavek": 
                self.doc["Pohledavky"]["Pocet_pohledavek"],
            "celkova_vyse":
                self.doc["Pohledavky"]["Celkova_vyse"],
            "celkova_vyse_nezajistenych":
                self.doc["Pohledavky"]["Celkova_vyse_nezajistenych"],
            "celkova_vyse_zajistenych":
                self.doc["Pohledavky"]["Celkova_vyse_zajistenych"],
        })

        pohledavky = []
        for pohledavka in self.doc["Pohledavky"]["Pohledavky"]:
            
            pohledavky.append({
                'pp_id'           : prihlaskaId,
                'cislo'           : pohledavka['Cislo'],
                'celkova_vyse'    : pohledavka['Celkova_vyse'],
                'vyse_jistiny'    : pohledavka['Vyse_jistiny'],
                'typ_text'        : pohledavka['Typ'][:50],
                'dalsi_okolnosti' : pohledavka['Dalsi_okolnosti'],
                'duvod_vzniku'    : pohledavka['Duvod_vzniku'],
                'splatna'         : pohledavka['Vlastnosti']['Splatna'],
                'podrizena'       : pohledavka['Vlastnosti']['Podrizena'],
                'vykonatelnost'   : bool(pohledavka['Vykonatelnost']),
            })

        await self.insertMany("pp_pohledavka", pohledavky)