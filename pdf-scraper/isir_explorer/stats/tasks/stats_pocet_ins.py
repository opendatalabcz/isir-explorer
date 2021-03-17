import json
from ..task import Task


class StatsPocetIns(Task):

    async def run(self):
        rows = await self.db.fetch_all(
            query="""SELECT to_char(datum_zahajeni,'YYYY-MM') as rok_mesic,
                        COUNT(*) AS c
                    FROM stat_vec
                    GROUP BY rok_mesic
                    ORDER BY rok_mesic ASC
                    """
        )

        data = {}
        for row in rows:
            data[row["rok_mesic"]] = row["c"]
        
        await self.db.execute(
            query="""INSERT INTO statistiky
            (nazev, rok, data)
        VALUES
            (:nazev, :rok, :data)""",
            values={
                "nazev": "stat.pocet.ins",
                "rok": "2019",
                "data": json.dumps(data),
            }
        )