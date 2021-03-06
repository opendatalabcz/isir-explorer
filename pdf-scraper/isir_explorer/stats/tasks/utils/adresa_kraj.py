import re
import csv
import os


class AdresaKraj:

    RIMSKE_CISLICE = {'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii',
                      'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx', 'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi',
                      'xxvii', 'xxviii', 'xxix', 'xxx', 'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi', 'xxxvii'}

    KRAJE_REF = {
        'Praha': 'PR',
        'Jihočeský kraj': 'JC',
        'Jihomoravský kraj': 'JM',
        'Karlovarský kraj': 'KA',
        'Kraj Vysočina': 'VY',
        'Královéhradecký kraj': 'KR',
        'Liberecký kraj': 'LI',
        'Moravskoslezský kraj': 'MO',
        'Olomoucký kraj': 'OL',
        'Pardubický kraj': 'PA',
        'Plzeňský kraj': 'PL',
        'Středočeský kraj': 'ST',
        'Ústecký kraj': 'US',
        'Zlínský kraj': 'ZL',
    }

    def __init__(self, **kwargs):
        self.obce = {}
        self.psc = {}
        self.slovnikObci()

    def slovnikObci(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../datasets/cz-obce.csv')
        with open(filename, "r") as infile:
            reader = csv.reader(infile)
            next(reader, None)  # skip 1st
            for row in reader:
                nazev = row[1].lower()
                kraj = row[8]
                self.obce[nazev] = {"kraj": kraj,
                                    "kraj_ref": self.KRAJE_REF[kraj]}

        filename = os.path.join(dirname, '../../datasets/cz-psc-kraje.csv')
        with open(filename, "r") as infile:
            reader = csv.reader(infile)
            next(reader, None)  # skip 1st
            for row in reader:
                psc = row[0]
                okres = row[1]
                kraj = row[2]
                self.psc[psc] = {"okres": int(okres), "kraj": kraj}

    def najitKrajPresPsc(self, psc):
        if not psc:
            return None

        psc = re.sub(' +', '', psc)
        
        if not re.match("^[0-9]{5}$", psc):
            return None

        if psc in self.psc:
            return self.psc[psc]

        return None

    def najitKrajPresMesto(self, mesto):
        if not mesto:
            return None

        # odstranit dup. mezery
        mesto = re.sub(' +', ' ', mesto)
        # odstanit cislice
        mesto = ''.join([i for i in mesto if not i.isdigit()])
        # standardizace nazvu
        mesto = mesto.split(
            " - ")[0].split("–")[0].split(",")[0].lower().strip()
        # odstranit koncovky bez mezer
        mesto = mesto.replace("-město", "")
        mesto = mesto.replace("-staré město", "")
        mesto = mesto.replace("-nové město", "")
        mesto = mesto.replace("-předměstí", "")
        mesto = mesto.replace(".", "")

        # reseni pro tvary jako "pardubice-zelené předměstí", "lanškroun-žichlínské předměstí"
        if "-" in mesto and mesto not in self.obce:
            mesto = mesto.split("-")[0]

        # reseni pro tvary jako "liberec vi", "příbram viii" - odstranit rimskou cislici na konci nazvu
        if " " in mesto and mesto not in self.obce and mesto.split(" ")[-1] in self.RIMSKE_CISLICE:
            mesto = ' '.join(mesto.split(" ")[:-1])

        # caste chybne oznaceni
        if mesto == "frýdek":
            mesto = "frýdek-místek"

        kraj = None
        if mesto in self.obce:
            kraj = {"kraj": self.obce[mesto]["kraj_ref"], "okres": None}

        return kraj

    def najitKraj(self, psc, mesto):
        kraj = self.najitKrajPresPsc(psc)
        if kraj:
            return kraj

        kraj = self.najitKrajPresMesto(mesto)
        return kraj