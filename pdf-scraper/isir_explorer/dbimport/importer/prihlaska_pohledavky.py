from .isir_importer import IsirImporter


class PrihlaskaImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Přihláška pohledávky.
    """

    async def importDocument(self):

        # Pocet pohledavek nekdy neni vyplnen
        if self.doc["Pohledavky"]["Pocet_pohledavek"] is None:
            self.doc["Pohledavky"]["Pocet_pohledavek"] = len(self.doc["Pohledavky"]["Pohledavky"])

        rowid = await self.insert("prihlaska_pohledavky",{
            "pocet_pohledavek": 
                self.doc["Pohledavky"]["Pocet_pohledavek"],
            "celkova_vyse":
                self.doc["Pohledavky"]["Celkova_vyse"],
            "celkova_vyse_nezajistenych":
                self.doc["Pohledavky"]["Celkova_vyse_nezajistenych"],
            "celkova_vyse_zajistenych":
                self.doc["Pohledavky"]["Celkova_vyse_zajistenych"],
        })
        print(f"Row: {rowid}")