from .isir_importer import IsirImporter


class PrihlaskaImporter(IsirImporter):
    """Třída pro databázový import dokumentů typu Přihláška pohledávky.
    """

    TYP_DOKUMENTU = 1
    DRUH_OSOBY_DLUZNIK = 1
    DRUH_OSOBY_VERITEL = 3

    TYP_POHLEDAVKY = {
        "nezajištěná - jednotlivě": 1,
        "nezajištěná - hromadně": 2,
        "zajištěná majetkem dlužníka": 3,
        "nezajištěná majetkem dlužníka": 4,
        "zajištěná nejen majetkem dlužníka": 5,
        "uspokojovaná pouze z majetku poskytnutého k zajištění": 6,
    }

    def typPohledavky(self, typ):
        try:
            return self.TYP_POHLEDAVKY[typ]
        except KeyError:
            return None

    async def _importAdresyOsoby(self, idOsoby, adresa):
        data_sidlo = [
            "osoba_id": idOsoby
        ]

        try:
            data_sidlo["ulice"] = adresa["Ulice"] or None
        except:
            data_sidlo["ulice"] = None

        try:
            data_sidlo["cp"] = adresa["Cp"] or None
        except:
            data_sidlo["cp"] = None

        try:
            data_sidlo["co"] = adresa["Co"] or None
        except:
            data_sidlo["co"] = None

        try:
            data_sidlo["obec"] = adresa["Obec"] or None
        except:
            data_sidlo["obec"] = None

        try:
            data_sidlo["cast_obce"] = adresa["Cast_obce"] or None
        except:
            data_sidlo["cast_obce"] = None

        try:
            data_sidlo["stat"] = adresa["Stat"] or None
        except:
            data_sidlo["stat"] = None

        osobaId = await self.insert("pp_osoba_sidlo", data_sidlo)

    async def _importOsoby(self, druhOsobyRizeni, osoba):

        # Udaje o osobe nejsou k dispozici
        if len(osoba) < 2:
            return

        data_osoby = {
            "pp_id":
                self.prihlaskaId,
            "druhrolevrizeni": 
                druhOsobyRizeni,
        }

        if osoba["FO_PO"] == 1:
            data_key = "Fyzicka_osoba"
            data_osoby["druhosoby"] = 1
            try:
                data_osoby["nazevosoby"] = osoba["Fyzicka_osoba"]["Udaje"]["Prijmeni"] or None
            except:
                data_osoby["nazevosoby"] = None

            try:
                data_osoby["jmeno"] = osoba["Fyzicka_osoba"]["Udaje"]["Jmeno"] or None
            except:
                data_osoby["jmeno"] = None

            try:
                data_osoby["titulpred"] = osoba["Fyzicka_osoba"]["Udaje"]["Titul_pred"] or None
            except:
                data_osoby["titulpred"] = None

            try:
                data_osoby["titulza"] = osoba["Fyzicka_osoba"]["Udaje"]["Titul_za"] or None
            except:
                data_osoby["titulza"] = None

            try:
                data_osoby["rc"] = osoba["Fyzicka_osoba"]["Udaje"]["Rodne_cislo"] or None
            except:
                data_osoby["rc"] = None

            try:
                data_osoby["datumnarozeni"] = self.dateFormat(osoba["Fyzicka_osoba"]["Udaje"]["Datum_narozeni"]) or None
            except:
                data_osoby["datumnarozeni"] = None
        else:
            data_key = "Pravnicka_osoba"
            data_osoby["druhosoby"] = 3

            try:
                data_osoby["nazevosoby"] = osoba["Pravnicka_osoba"]["Udaje"]["Nazev"] or None
            except:
                data_osoby["nazevosoby"] = None

        try:
            data_osoby["cislo_uctu"] = osoba[data_key]["Udaje"]["Cislo_uctu"] or None
        except:
            data_osoby["cislo_uctu"] = None

        try:
            data_osoby["ic"] = str(osoba[data_key]["Udaje"]["IC"]) or None
        except:
            data_osoby["ic"] = None

        try:
            data_osoby["reg_cislo"] = osoba[data_key]["Udaje"]["Jine_reg_cislo"] or None
        except:
            data_osoby["reg_cislo"] = None

        if len(data_osoby["ic"]) > 9:
            data_osoby["ic"] = None
            if data_osoby["reg_cislo"] is None:
                data_osoby["reg_cislo"] = str(data_osoby["ic"])

        osobaId = await self.insert("pp_osoba", data_osoby)

        if "Sidlo" in osoba[data_key]["Udaje"]:
            await self._importAdresyOsoby(osobaId, osoba[data_key]["Udaje"]["Sidlo"])

    async def importDocument(self, dokumentId):

        # Pocet pohledavek nekdy neni vyplnen
        if self.doc["Pohledavky"]["Pocet_pohledavek"] is None:
            self.doc["Pohledavky"]["Pocet_pohledavek"] = len(self.doc["Pohledavky"]["Pohledavky"])

        self.prihlaskaId = await self.insert("prihlaska_pohledavky",{
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
                'pp_id'           : self.prihlaskaId,
                'cislo'           : pohledavka['Cislo'],
                'celkova_vyse'    : pohledavka['Celkova_vyse'],
                'vyse_jistiny'    : pohledavka['Vyse_jistiny'],
                'typ'             : self.typPohledavky(pohledavka['Typ']),
                'typ_text'        : pohledavka['Typ'][:50],
                'dalsi_okolnosti' : pohledavka['Dalsi_okolnosti'],
                'duvod_vzniku'    : pohledavka['Duvod_vzniku'],
                'splatna'         : pohledavka['Vlastnosti']['Splatna'],
                'podrizena'       : pohledavka['Vlastnosti']['Podrizena'],
                'vykonatelnost'   : bool(pohledavka['Vykonatelnost']),
            })

        await self.insertMany("pp_pohledavka", pohledavky)

        # Udaje o veriteli
        #await self._importOsoby(self.DRUH_OSOBY_DLUZNIK, self.doc["Dluznik"]) # neni treba evidovat
        await self._importOsoby(self. DRUH_OSOBY_VERITEL, self.doc["Veritel"])
       