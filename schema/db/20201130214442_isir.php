<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class Isir extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('isir_udalost', ['id' => false, 'primary_key' => ['spisovaznacka', 'oddil', 'cislovoddilu', 'typudalosti']]);
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('soud', 'smallinteger', ['null' => true])
              ->addColumn('spisovaznacka', 'string', ['null' => false, 'limit'=>50])
              ->addColumn('oddil', 'string', ['null' => false, 'limit'=>10])
              ->addColumn('cislovoddilu', 'smallinteger', ['null' => false])
              ->addColumn('typudalosti', 'smallinteger', ['null' => false])
              ->addColumn('dokumenturl', 'string', ['null' => true, 'limit' => 100])
              ->addColumn('datumzalozeniudalosti', 'timestamp', ['null' => true])
              ->addColumn('datumzverejneniudalosti', 'timestamp', ['null' => true])
              ->addColumn('poznamka_json', 'text', ['null' => true])
              ->addColumn('priznakanvedlejsiudalost', 'boolean', ['null' => true])
              ->addColumn('priznakanvedlejsidokument', 'boolean', ['null' => true])
              ->addColumn('priznakplatnyveritel', 'boolean', ['null' => true])
              ->addColumn('priznakmylnyzapisveritelpohled', 'boolean', ['null' => true])
              ->addColumn('stav', 'smallinteger', ['null' => true])
              ->addColumn('pocet_zmen', 'smallinteger', ['null' => true, 'default'=>0])
              ->addColumn('dl_precteno', 'timestamp', ['null' => true, 'comment'=>'Datum scrapovani asociovaneho PDF dokumentu'])
              ->addIndex(['id'], ['unique' => true])
              ->addIndex(['spisovaznacka', 'oddil', 'cislovoddilu', 'typudalosti'], ['unique' => true])
              ->create();

        $table = $this->table('isir_osoba', ['id' => false, 'primary_key' => ['spisovaznacka', 'idosoby']]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit'=>50])
              ->addColumn('idosoby', 'string', ['null' => false])
              ->addColumn('soud', 'smallinteger', ['null' => true])
              ->addColumn('druhrolevrizeni', 'smallinteger', ['null' => true])
              ->addColumn('druhspravce', 'smallinteger', ['null' => true])
              ->addColumn('nazevosoby', 'string', ['null' => true, 'limit'=>255])
              ->addColumn('nazevosobyobchodni', 'string', ['null' => true, 'limit'=>255])
              ->addColumn('druhosoby', 'smallinteger', ['null' => true])
              ->addColumn('druhpravniforma', 'smallinteger', ['null' => true])
              ->addColumn('jmeno', 'string', ['null' => true, 'limit'=>255])
              ->addColumn('titulpred', 'string', ['null' => true, 'limit'=>50])
              ->addColumn('titulza', 'string', ['null' => true, 'limit'=>50])
              ->addColumn('ic', 'string', ['null' => true, 'limit'=>9])
              ->addColumn('dic', 'string', ['null' => true, 'limit'=>14])
              ->addColumn('rc', 'string', ['null' => true, 'limit'=>11])
              ->addColumn('datumosobavevecizrusena', 'timestamp', ['null' => true])
              ->addColumn('datumnarozeni', 'date', ['null' => true])
              ->addColumn('datumzalozeni', 'timestamp', ['null' => true])
              ->addColumn('idzalozeni', 'integer', ['null' => true])
              ->addColumn('edits', 'smallinteger', ['null' => true, 'default'=>0])

              ->addIndex(['ic'], ['unique' => false])
              ->addIndex(['rc'], ['unique' => false])
              ->addIndex(['nazevosoby', 'jmeno', 'datumnarozeni'], ['unique' => false])

              ->create();

        $table = $this->table('isir_vec', ['id' => false, 'primary_key' => ['spisovaznacka']]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit'=>50])
              ->addColumn('druhstavrizeni', 'smallinteger', ['null' => false])
              ->addColumn('datumveczrusena', 'string', ['null' => true])
              ->addColumn('datumkoneclhutyprihlasek', 'timestamp', ['null' => true])
              ->addColumn('datumskonceniveci', 'timestamp', ['null' => true])
              ->addColumn('datumaktualizace', 'timestamp', ['null' => true])
              ->addColumn('edits', 'smallinteger', ['null' => false, 'default'=>0])
              ->create();

        $table = $this->table('isir_vec_stav');
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit'=>50])
            ->addColumn('druhstavrizeni', 'smallinteger', ['null' => false])
            ->addColumn('datum', 'timestamp', ['null' => false])
            ->addColumn('rid', 'integer', ['null' => true])
            ->addIndex(['spisovaznacka'], ['unique' => false])
            ->create();
    }
}
