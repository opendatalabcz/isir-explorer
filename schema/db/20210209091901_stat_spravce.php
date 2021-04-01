<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class StatSpravce extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('stat_spravce', [
            'comment' => 'Seznam ins. správců získaný z existujících řízení'
        ]);
        $table->addColumn('ic', 'string', ['null' => true, 'limit' => 9, 'comment' => 'Identifikacni cislo (pravnicka osoba nebo fyz. osoba podnikatel)'])
            ->addColumn('nazev', 'string', ['null' => false, 'comment' => 'Plne jmeno (s tituly) nebo obchodni nazev spravce'])
            ->addColumn('jmeno', 'string', ['null' => true, 'comment' => 'Jmeno, pokud nejde o pravnickou osobu'])
            ->addColumn('prijmeni', 'string', ['null' => true, 'comment' => 'Prijmeni, pokud nejde o pravnickou osobu'])
            ->addColumn('posledni_ins', 'date', ['null' => true, 'comment' => 'Datum prirazeni posledni insolvence'])
            ->addColumn('ins_celkem', 'smallinteger', ['null' => true, 'comment' => 'Pocet vsech insolvenci spravce'])
            ->addColumn('ins_aktivnich', 'smallinteger', ['null' => true, 'comment' => 'Pocet aktualne probihajicich insolvenci'])

            ->addIndex(['ic'], ['unique' => false])

            ->create();

        // ----------------------------------------------------------------------

        $table = $this->table('stat_vec', [
            'comment' => 'Seznam ins. rizeni se statistikymi informacemi o nich'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])
            ->addColumn('typ_osoby', 'string', ['limit' => 1, 'null' => true, 'comment' => 'Osoba dluznika, F=fyzicka, P=pravnicka'])
            ->addColumn('podnikatel', 'boolean', ['null' => true, 'comment' => 'Je osoba dluznika podnikatel'])
            ->addColumn('vek_dluznika', 'smallinteger', ['null' => true, 'comment' => 'Vek dluznika v dobe zahajeni rizeni'])
            ->addColumn('pohlavi_dluznika', 'string', ['limit' => 1, 'null' => true, 'comment' => 'M=muz, Z=zena'])
            ->addColumn('typ_rizeni', 'string', ['limit' => 1, 'null' => true, 'comment' => 'Konstanta oznacujici zpusob reseni upadku'])
            ->addColumn('kraj', 'string', ['limit' => 2, 'null' => true, 'comment' => 'Kod kraje, ze ktereho pochazi dluznik'])
            ->addColumn('okres', 'smallinteger', ['null' => true, 'comment' => 'Kod okresu, ze ktereho pochazi dluznik'])
            ->addColumn('moratorium', 'date', ['null' => true, 'comment' => 'Datum, kdy bylo v rizeni vyhlaseno moratorium'])
            ->addColumn('datum_zahajeni', 'date', ['null' => true, 'comment' => 'Datum zacatku rizeni'])
            ->addColumn('datum_upadku', 'date', ['null' => true, 'comment' => 'Datum vydani rozhodnuti o upadku'])
            ->addColumn('datum_zpusob_reseni', 'date', ['null' => true, 'comment' => 'Datum, kdy byl stanoven zpusob reseni upadku'])
            ->addColumn('datum_ukonceni', 'date', ['null' => true, 'comment' => 'Datum konce rizeni'])
            ->addColumn('delka_rizeni', 'smallinteger', ['null' => true, 'comment' => 'Doba trvani rizeni (Pocet dnu)'])

            ->addForeignKey('spisovaznacka', 'isir_vec', 'spisovaznacka', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['spisovaznacka'], ['unique' => true])

            ->create();

        // ----------------------------------------------------------------------

        $table = $this->table('stat_spravce_ins', [
            'comment' => 'Vazby mezi spravci a jejich rizenimi, a statistiky prislusnych vazeb',
            'id' => false,
            'primary_key' => ['id_spravce', 'id_ins'],
        ]);

        $table->addColumn('id_spravce', 'integer', ['null' => false])
            ->addColumn('id_ins', 'integer', ['null' => false])
            ->addColumn('druh_spravce', 'smallinteger', ['null' => false, 'comment' => '1=INS, 2=ZVL, 3=ZÁST'])
            ->addColumn('celkova_odmena', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Celkova odmena spravce (je-li udaj dostupny)'])

            ->addForeignKey('id_spravce', 'stat_spravce', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addForeignKey('id_ins', 'stat_vec', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])

            ->create();

        $table = $this->table('isir_vec');
        $table->addColumn('vyrazeno', 'boolean', ['null'=>false, 'default' => false, 'comment' => 'Vyradit rizeni z tvorby statistik'])
                ->update();
    }
}
