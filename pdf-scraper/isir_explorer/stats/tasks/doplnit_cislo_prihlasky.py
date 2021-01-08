import os
import json
import re
from databases import Database
from ..task import Task

class DoplnitCisloPrihlasky(Task):

    async def run(self):
        rows = await self.db.fetch_all(query="""
                SELECT *, pp.id AS pp_id FROM prihlaska_pohledavky pp
                    LEFT JOIN dokument ON (dokument.id = pp.id)
                    LEFT JOIN isir_udalost ON (dokument.isir_id = isir_udalost.dokumenturl AND isir_udalost.typudalosti=63)
                WHERE
                    pp.cislo_prihlasky IS NULL
                ORDER BY pp.id ASC
            """)
        i = 0
        for row in rows:
            if row["oddil"] and row["oddil"][0] == "P":
                try:
                    cislo_prihlasky = int(row["oddil"][1:])
                except:
                    continue
                
                i += 1
                await self.db.execute(query="""
                    UPDATE prihlaska_pohledavky SET cislo_prihlasky=:cislo_prihlasky WHERE id=:pp_id
                """, values={
                    "pp_id": row["pp_id"],
                    "cislo_prihlasky": cislo_prihlasky,
                })

                if i % 1000 == 0:
                    print("Zpracovano {0} ...".format(i))


