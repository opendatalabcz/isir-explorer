from .helpers import *
from .enums import *
import re
import xml.etree.ElementTree as ET
import dateutil.parser
from datetime import datetime
import json
import time


class IsirModel:

    ATTRS = []
    IGNORED = []
    IGNORE_IN_UPDATE = []
    COMPUTED_FIELDS = []
    FLAGS = []
    COUNT_EDITS = True
    TABLE_NAME = ""

    def __init__(self, xml_elem, record=None):
        self.data = {}
        if record is not None:
            self.record = record

        for e in self.ATTRS:
            if e not in self.COMPUTED_FIELDS:
                data = self.child_text(xml_elem, e)
                self.data[e] = self.format_column(e, data)

        for e in self.COMPUTED_FIELDS:
            method_to_call = getattr(self, e)
            self.data[e] = method_to_call()

        for e in self.FLAGS:
            elem = self.poznamka.find(e)
            if elem is not None:
                self.data[e] = False if elem.text in ["F", "f"] else True
            else:
                self.data[e] = None

        if record is not None:
            self.spisovaZnacka = record.spisovaZnacka

    @staticmethod
    def child_text(parent, elemName):
        elem = parent.find(elemName)
        if elem is None:
            return None
        return elem.text

    @staticmethod
    def format_column(columnName, data):
        return data

    @classproperty
    def db_columns(cls):
        return [item for item in cls.ATTRS if item not in cls.IGNORED]

    def __getattr__(self, attr_name):
        try:
            return self.data[attr_name]
        except KeyError:
            raise AttributeError(attr_name)

    def __setattr__(self, name, value):
        if name in self.ATTRS:
            self.data[name] = value
        else:
            super().__setattr__(name, value)

    @classmethod
    def get_insert_query(cls, dialect):
        column_order = ",".join(cls.db_columns)
        
        column_placeholders_list = []
        for c in cls.db_columns:
            column_placeholders_list.append(":"+c)
        column_placeholders = ",".join(column_placeholders_list)

        update_part = ""
        i = 0
        for a in cls.db_columns:
            if a in cls.IGNORE_IN_UPDATE:
                continue
            if i != 0:
                update_part += ", "
            update_part += f"{a}=:{a}"
            i += 1

        if "mysql" == dialect:
            edit_counter = ", pocet_zmen=pocet_zmen+1" if cls.COUNT_EDITS else ""
            return f"INSERT INTO {cls.TABLE_NAME} ({column_order}) VALUES ({column_placeholders}) " \
                f"ON DUPLICATE KEY UPDATE {update_part} {edit_counter}"
        else:
            edit_counter = ", pocet_zmen=EXCLUDED.pocet_zmen+1" if cls.COUNT_EDITS else ""
            return f"INSERT INTO {cls.TABLE_NAME} ({column_order}) VALUES ({column_placeholders}) " \
                f"ON CONFLICT {cls.UNIQUE_CONSTRAINT} DO UPDATE SET {update_part} {edit_counter}"

    @staticmethod
    def get_enum(enum, val):
        try:
            return enum[val]
        except KeyError:
            print(f"Enum error: \"{val}\" not in enum ({list(enum.keys())[0]},...)")
            return 0            # Unknown

    @staticmethod
    def parse_datetime(data):
        if isinstance(data, datetime):
            return data
        dt = dateutil.parser.parse(data)
        if dt.year > 2035:  # unix timestamp limits
            dt = dt.replace(year=2035)
        elif dt.year < 1999:
            dt = dt.replace(year=2000)
        res = dt.strftime('%Y-%m-%d %H:%M:%S')

        try:
            datetimeobject = datetime.strptime(res, '%Y-%m-%d %H:%M:%S')
        except:
            return None
        return datetimeobject

    def get_db_data(self):
        data = {}
        for item in self.db_columns:
            try:
                data[item] = self.data[item]
            except KeyError:
                data[item] = None
        return data

class IsirUdalost(IsirModel):

    ATTRS = ['id', 'spisovaZnacka', 'oddil', 'cisloVOddilu', 'typUdalosti', 'dokumentUrl',
             'datumZalozeniUdalosti', 'datumZverejneniUdalosti', 'poznamka', 'poznamka_json',
             'priznakAnVedlejsiUdalost', 'priznakAnVedlejsiDokument',
             'priznakPlatnyVeritel', 'priznakMylnyZapisVeritelPohled', 'stav', 'soud']
    IGNORED = ['poznamka']
    IGNORE_IN_UPDATE = ['id', 'spisovaZnacka', 'oddil', 'cisloVOddilu', 'typUdalosti','datumZalozeni']
    TABLE_NAME = "isir_udalost"
    UNIQUE_CONSTRAINT = "ON CONSTRAINT isir_udalost_pkey"
    COMPUTED_FIELDS = ['poznamka_json', 'stav', 'soud']

    UDALOST_FIELDS = ['datumUdalostZrusena', 'datumPravniMoci',
                      'datumSpojeni', 'datumOddeleni',
                      'druhOddilPrihl', 'cisloOddiluPrihl', 'osobaVeritel',
                      'datumVyskrtnuti', 'idOsoby1', 'idOsoby2', 'datumZverejneniOpraveneUdalosti']

    FLAGS = ['priznakAnVedlejsiUdalost', 'priznakAnVedlejsiDokument',
             'priznakPlatnyVeritel', 'priznakMylnyZapisVeritelPohled']

    DOC_PREFIX = "https://isir.justice.cz:8443/isir_public_ws/doc/Document?idDokument="

    def poznamka_json(self):
        j = {}

        for e in self.UDALOST_FIELDS:
            elem = self.poznamka.find(e)
            if elem is not None:
                j[e] = elem.text

        if len(j) == 0:
            return None

        return json.dumps(j)

    def stav(self):
        vec = self.poznamka.find("vec")
        res = None
        if vec is not None:
            elem = vec.find("druhStavRizeni")
            if elem is not None:
                res = IsirModel.get_enum(DRUH_STAV_RIZENI, elem.text)
                if vec.find("datumVecZrusena") is not None:
                    res += 128
        return res

    def soud(self):
        elem = self.poznamka.find("idOsobyPuvodce")
        if elem is not None:
            return IsirModel.get_enum(SOUDY, elem.text)
        else:
            return None

    @staticmethod
    def format_column(columnName, data):
        if columnName[0:5] == "datum":
            return IsirModel.parse_datetime(data)
        elif columnName == "typUdalosti" and data is not None:
            return int(data)
        elif columnName == "cisloVOddilu" and data is not None:
            return int(data)
        elif columnName == "id":
            return int(data)
        elif columnName == "dokumentUrl" and data is not None:
            if data.startswith(IsirUdalost.DOC_PREFIX):
                return data[len(IsirUdalost.DOC_PREFIX):]  # store only the unique part of the url to save space
            else:
                return data
        elif columnName == "poznamka":
            return ET.fromstring(data)
        return data


class IsirOsoba(IsirModel):

    ATTRS = ['spisovaZnacka', 'idOsoby', 'druhRoleVRizeni', 'druhSpravce', 'nazevOsoby', 'nazevOsobyObchodni',
             'druhOsoby', 'druhPravniForma', 'jmeno', 'titulPred', 'titulZa', 'ic', 'dic', 'rc',
             'datumOsobaVeVeciZrusena', 'datumNarozeni', 'soud', 'datumZalozeni', 'idZalozeni']
    IGNORE_IN_UPDATE = ['spisovaZnacka', 'idOsoby', 'datumZalozeni', 'idZalozeni']
    TABLE_NAME = "isir_osoba"
    UNIQUE_CONSTRAINT = "(spisovaznacka, idosoby)"

    @staticmethod
    def format_column(columnName, data):
        if data is None:
            return data
        if columnName == "datumNarozeni":
            res = data[0:10]               # date returned by ISIR as "1979-05-16+02:00"
            try:
                datetimeobject = datetime.strptime(res, '%Y-%m-%d')
            except:
                return None
            return datetimeobject

        elif columnName[0:5] == "datum":
            return IsirModel.parse_datetime(data)
        elif columnName == "idZalozeni" and data is not None:
            return int(data)
        elif columnName == "idOsoby":
            return re.sub(r'[ ]+', '-', data)
        elif columnName == "druhRoleVRizeni":
            return IsirModel.get_enum(DRUH_ROLE_V_RIZENI, data)
        elif columnName == "druhSpravce":
            return IsirModel.get_enum(DRUH_SPRAVCE, data)
        elif columnName == "druhOsoby":
            return IsirModel.get_enum(DRUH_OSOBY, data)
        elif columnName == "druhPravniForma":
            return IsirModel.get_enum(DRUH_PRAVNI_FORMA, data)
        elif columnName == "druhRoleVRizeni":
            return IsirModel.get_enum(DRUH_ROLE_V_RIZENI, data)
        return data

class IsirVec(IsirModel):

    ATTRS = ['spisovaZnacka', 'druhStavRizeni', 'datumVecZrusena', 'datumKonecLhutyPrihlasek', 'datumSkonceniVeci', 'datumAktualizace']
    IGNORE_IN_UPDATE = ['spisovaZnacka']
    COMPUTED_FIELDS = ['datumAktualizace']
    TABLE_NAME = "isir_vec"
    UNIQUE_CONSTRAINT = "ON CONSTRAINT isir_vec_pkey"

    @staticmethod
    def format_column(columnName, data):
        if data is None:
            return data
        if columnName == "druhStavRizeni":
            return IsirModel.get_enum(DRUH_STAV_RIZENI, data)
        elif columnName[0:5] == "datum":
            return IsirModel.parse_datetime(data)
        return data

    def datumAktualizace(self):
        return IsirModel.parse_datetime(self.record.datumZalozeniUdalosti)


class IsirStavVeci(IsirModel):

    ATTRS = ['spisovaZnacka', 'druhStavRizeni', 'datum', 'rid']
    TABLE_NAME = "isir_vec_stav"
    UNIQUE_CONSTRAINT = "ON CONSTRAINT isir_vec_stav_pkey"
    COMPUTED_FIELDS = ['datum', 'rid']
    COUNT_EDITS = False

    @staticmethod
    def format_column(columnName, data):
        if data is None:
            return data
        if columnName == "druhStavRizeni":
            return IsirModel.get_enum(DRUH_STAV_RIZENI, data)
        return data

    def datum(self):
        return IsirModel.parse_datetime(self.record.datumZalozeniUdalosti)

    def rid(self):
        return self.record.id
