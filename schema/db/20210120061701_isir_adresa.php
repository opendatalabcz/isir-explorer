<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class IsirAdresa extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('isir_adresa', [
            'comment' => 'Adresy subjektů z isir_isoba (zdroj: isir-ws)'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])
            ->addColumn('idosoby', 'string', ['null' => false, 'comment' => 'Identifikator osoby prirazeny webovou sluzbou MSp'])
            ->addColumn('isir_osoba', 'integer', ['null' => true, 'comment' => 'Asociace isir_osoba'])
            ->addColumn('idadresy', 'integer', ['null' => false, 'comment' => 'Id adresy prirazene webovou sluzbou MSp, unikatni pouze v ramci rizeni'])
            ->addColumn('druhadresy', 'smallinteger', ['null' => false, 'comment' => '8=trvala, 7=sidlo org, 6=sidlo firm, ... dale viz webservice.enums'])
            
            ->addColumn('datumpobytod', 'date', ['null' => true, 'comment' => 'Datum začátku platnosti adresy'])
            ->addColumn('datumpobytdo', 'date', ['null' => true, 'comment' => 'Datum konce platnosti adresy'])
            ->addColumn('mesto', 'string', ['null' => true, 'limit' => 255])
            ->addColumn('ulice', 'string', ['null' => true, 'limit' => 255])
            ->addColumn('cislopopisne', 'string', ['null' => true, 'limit' => 10])
            ->addColumn('okres', 'string', ['null' => true, 'limit' => 30])
            ->addColumn('zeme', 'string', ['null' => true, 'limit' => 255])
            ->addColumn('psc', 'string', ['null' => true, 'limit' => 6])
            ->addColumn('telefon', 'string', ['null' => true, 'limit' => 30])
            ->addColumn('fax', 'string', ['null' => true, 'limit' => 30])
            ->addColumn('textadresy', 'string', ['null' => true, 'limit' => 255, 'comment' => 'text adresy e-mailu, URL apod'])
            ->addColumn('pocet_zmen', 'smallinteger', ['null' => true, 'default' => 0, 'comment' => 'Kolikrat byl zaznam teto adresy v rejstriku zmenen'])
            
            ->addForeignKey('isir_osoba', 'isir_osoba', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['spisovaznacka', 'idadresy'], ['unique' => true])

            ->create();
    }
}
