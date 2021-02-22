import json
from ..task import Task
from .utils.adresa_kraj import AdresaKraj


class StatsKrajeRizeni(Task):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

        self.neprirazeno = 0
        self.pocty_kraje = {}
        self.AdresaKraj = AdresaKraj()

    async def run(self):

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

        for row in rows:
            kraj = self.AdresaKraj.najitKraj(row["adresa_mesto"])
            if kraj:
                if kraj in self.pocty_kraje:
                    self.pocty_kraje[kraj] += 1
                else:
                    self.pocty_kraje[kraj] = 1
            else:
                self.neprirazeno += 1
                print("Nenalezeno: {0}".format(row["adresa_mesto"]))

        print(f"Nenalezeno celkem: {self.neprirazeno}")
        print(json.dumps(self.pocty_kraje))
