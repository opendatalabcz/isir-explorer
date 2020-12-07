from .isir_importer import IsirImporter


class PrehledovyListImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Přehledový list.
    """

    TYP_DOKUMENTU = 2

    def sumarizaceTypuVeritele(self, jeZajisteny, celkem):
        if len(celkem) < 1:
            return {}

        col_prefix = 'z_' if jeZajisteny else 'n_'
        
        res = {
            'celkova_vyse': celkem["Celkova_vyse"],
            'vykonatelne': celkem["Vykonatelne"],
            'nevykonatelne': celkem["Nevykonatelne"],
            'duplicitni': celkem["Duplicitni"],
            'neprezkoumavano': celkem["Neprezkoumavano"],
            'odmitnuto': celkem["Odmitnuto"],
            'podmineno': celkem["Podmineno"],
            'popreno': celkem["Popreno"],
            'zbyva_uspokojit': celkem["Zbyva_uspokojit"],
            'zjisteno': celkem["Zjisteno"],
        }

        return {col_prefix+k : v for k,v in res.items()}

    def pohledavky(self, prehledovyListId, jeZajisteny, pohledavky):

        res = []
        for pohledavka in pohledavky:
            res.append({
                'pl_id': prehledovyListId,
                'typ': jeZajisteny,
                'celkova_vyse': pohledavka['Celkova_vyse'],
                'cislo_prihlasky': pohledavka['Cislo_prihlasky'],
                'cislo_veritele': pohledavka['Cislo_veritele'],
                'datum_doruceni': self.dateFormat(pohledavka['Datum_doruceni']),
                'duplicitni': pohledavka['Duplicitni'],
                'neprezkoumavano': pohledavka['Neprezkoumavano'],
                'nevykonatelne': pohledavka['Nevykonatelne'],
                'odmitnuto': pohledavka['Odmitnuto'],
                'podmineno': pohledavka['Podmineno'],
                'popreno': pohledavka['Popreno'],
                'procent': pohledavka['Procent'],
                'veritel': pohledavka['Veritel'],
                'vykonatelne': pohledavka['Vykonatelne'],
                'zbyva_uspokojit': pohledavka['Zbyva_uspokojit'],
                'zjisteno': pohledavka['Zjisteno'],
            })
        return res


    async def importDocument(self, dokumentId):

        # Vlozit prehledovy list
        nezajistene = self.sumarizaceTypuVeritele(False, self.doc["Nezajistene"]["Celkem"])
        zajistene = self.sumarizaceTypuVeritele(True, self.doc["Zajistene"]["Celkem"])
        # data radku tabulky
        prehledovyList = {
            "id": dokumentId,
            **nezajistene,
            **zajistene
        }
        prehledovyListId = await self.insert("prehledovy_list", prehledovyList)

        # Vlozit pohledavky k prehledovemu listu
        pohledavky_nezajistene = self.pohledavky(prehledovyListId, False, self.doc["Nezajistene"]["Pohledavky"])
        pohledavky_zajistene = self.pohledavky(prehledovyListId, True, self.doc["Zajistene"]["Pohledavky"])
        pohledavky = pohledavky_nezajistene + pohledavky_zajistene
        await self.insertMany("pl_pohledavka", pohledavky)