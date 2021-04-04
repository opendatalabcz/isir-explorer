from ..task import Task


class StatsInsVecDatum(Task):

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)

    async def seznamInsRizeni(self):
        return await self.db.fetch_all(query="""
            SELECT * FROM stat_vec WHERE zahajeni_r IS NULL OR ukonceni_r IS NULL
        """)

    async def analyzaRizeni(self, stat_vec):
        zahajeni_r = None
        zahajeni_m = None
        ukonceni_r = None
        ukonceni_m = None

        if stat_vec["datum_zahajeni"]:
            zahajeni_r = stat_vec["datum_zahajeni"].year
            zahajeni_m = stat_vec["datum_zahajeni"].month

        if stat_vec["datum_ukonceni"]:
            ukonceni_r = stat_vec["datum_ukonceni"].year
            ukonceni_m = stat_vec["datum_ukonceni"].month

        await self.db.execute(
            query="""UPDATE stat_vec
            SET
            zahajeni_r=:zahajeni_r,
            zahajeni_m=:zahajeni_m,
            ukonceni_r=:ukonceni_r,
            ukonceni_m=:ukonceni_m
            WHERE spisovaznacka=:spisovaznacka
            """,
            values={
                "spisovaznacka": stat_vec["spisovaznacka"],
                "zahajeni_r": zahajeni_r,
                "zahajeni_m": zahajeni_m,
                "ukonceni_r": ukonceni_r,
                "ukonceni_m": ukonceni_m,
            }
        )

    async def run(self):
        rows = await self.seznamInsRizeni()
        await self.analyzaRizeni(dict(row))
        print("Zpracovano {0} ...".format(count(rows)))
