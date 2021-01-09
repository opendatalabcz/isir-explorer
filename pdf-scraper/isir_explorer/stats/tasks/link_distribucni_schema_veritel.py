import os
import json
import re
from databases import Database
from ..task import Task

class LinkDistribucniSchemaVeritel(Task):

    async def run(self):
        print("Hledani asociace ...")
        rows = await self.db.fetch_all(query="""
                SELECT ds.id as ds_id, veritel, isir_osoba.id AS osoba_id FROM zpro_distribucni_schema ds
                LEFT JOIN dokument ON (ds.zpro_id = dokument.id)
                LEFT JOIN isir_osoba ON (isir_osoba.spisovaznacka = dokument.spisova_znacka AND isir_osoba.cislo_veritele = ds.veritel)
                WHERE osoba_spojena IS NULL AND idosoby IS NOT NULL
            """)
        print("Probiha spojovani ...")
        i = 0
        for row in rows:
            i += 1
            await self.db.execute(query="""
                UPDATE zpro_distribucni_schema SET veritel_id=:veritel_id, osoba_spojena=1 WHERE id=:ds_id
            """, values={
                "veritel_id": row["osoba_id"],
                "ds_id": row["ds_id"],
            })

            if i % 1000 == 0:
                print("Zpracovano {0} ...".format(i))


