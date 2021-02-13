import os
import json
import re
import csv
from databases import Database
from ..task import Task

class StatsKrajeRizeni(Task):
    """2019: 1710718 radku -> 64463 -> 96.2% zaznamu bylo redundantnich
    """

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

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.neprirazeno = 0
        self.obce = {}
        self.pocty_kraje = {}

    def slovnikObci(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../datasets/cz-obce.csv')
        with open(filename, "r") as infile:
            reader = csv.reader(infile)
            next(reader, None)  # skip 1st
            for row in reader:
                nazev = row[1].lower()
                kraj = row[8]
                self.obce[nazev] = {"kraj": kraj, "kraj_ref": self.KRAJE_REF[kraj]}

    async def run(self):
        self.slovnikObci()

        rows = await self.db.fetch_all(query="""
                SELECT * FROM (
                    SELECT io.idosoby, (
                        SELECT mesto FROM isir_adresa ia
                        WHERE
                            ia.idosoby = io.idosoby AND
                            ia.spisovaznacka = io.spisovaznacka AND
                            (ia.zeme IS NULL OR ia.zeme = 'Česká republika')
                        ORDER BY druhadresy DESC, id ASC LIMIT 1) as adresa_mesto
                    FROM isir_osoba io
                    JOIN isir_vec iv ON (io.spisovaznacka = iv.spisovaznacka)
                    WHERE
                        io.druhrolevrizeni = 1 AND to_char(iv.datumzahajeni, 'YYYY-MM') = '2019-12'
                    ) a
                WHERE adresa_mesto IS NOT NULL
            """)
        i = 0
        for row in rows:
            
            mesto = row["adresa_mesto"]

            # odstranit dup. mezery
            mesto = re.sub(' +', ' ', mesto)
            # odstanit cislice
            mesto = ''.join([i for i in mesto if not i.isdigit()])
            # standardizace nazvu
            mesto = mesto.split(" - ")[0].split("–")[0].split(",")[0].lower().strip()
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

            if mesto in self.obce:
                kraj = self.obce[mesto]["kraj_ref"]
                if kraj in self.pocty_kraje:
                    self.pocty_kraje[kraj] += 1
                else:
                    self.pocty_kraje[kraj] = 1
            else:
                self.neprirazeno += 1
                print(f"Nenalezeno: {mesto}")
            
        print(f"Nenalezeno celkem: {self.neprirazeno}")
        print(json.dumps(self.pocty_kraje))

