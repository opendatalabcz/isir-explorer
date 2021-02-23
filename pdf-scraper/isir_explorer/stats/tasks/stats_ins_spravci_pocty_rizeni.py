from ..task import Task


class StatsInsSpravciPoctyRizeni(Task):

    async def run(self):

        spravci = await self.db.fetch_all(query="""
                SELECT * FROM stat_spravce
            """)

        for spravce in spravci:
            data = await self.db.fetch_one(query="""
                SELECT COUNT(*) AS celkem, MAX(sv.datum_zahajeni) AS posledni FROM stat_spravce ss
                JOIN stat_spravce_ins ssi ON (ssi.id_spravce = ss.id)
                JOIN stat_vec sv ON (sv.id = ssi.id_ins)
                WHERE ss.id = :id
                """, values={"id": spravce["id"]}
            )

            celkem = data["celkem"]
            posledni = data["posledni"]

            data = await self.db.fetch_one(query="""
                SELECT COUNT(*) AS aktivnich FROM stat_spravce ss
                JOIN stat_spravce_ins ssi ON (ssi.id_spravce = ss.id)
                JOIN stat_vec sv ON (sv.id = ssi.id_ins)
                WHERE ss.id = :id AND sv.datum_ukonceni IS NULL
                """, values={"id": spravce["id"]}
            )

            aktivnich = data["aktivnich"]

            await self.db.execute(query="""UPDATE stat_spravce
                SET posledni_ins=:posledni_ins,	ins_celkem=:ins_celkem, ins_aktivnich=:ins_aktivnich
                WHERE id=:id
                """,
                values={
                    "posledni_ins": posledni,
                    "ins_celkem": celkem,
                    "ins_aktivnich": aktivnich,
                    "id": spravce["id"],
                }
            )