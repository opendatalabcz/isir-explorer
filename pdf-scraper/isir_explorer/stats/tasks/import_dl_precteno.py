from ..task import Task

import csv
import dateutil.parser


class ImportDlPrecteno(Task):

    async def run(self):
        # isir_udalost.id, dl_precteno
        with open('dump.csv', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        i = 0
        for row in rows:
            i += 1
            await self.db.execute(query="""
                UPDATE isir_udalost SET dl_precteno=:dl_precteno WHERE id=:id
            """, values={
                "id": int(row[0]),
                "dl_precteno": dateutil.parser.parse(row[1]),
            })

            if i % 1000 == 0:
                print("Zpracovano {0} ...".format(i))
