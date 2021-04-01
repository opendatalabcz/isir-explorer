<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class StatSpravce extends AbstractMigration
{
    public function change(): void
    {

        $table = $this->table('stat_vec', [
            'comment' => 'Statistiky pohledavek u jednotlivych rizeni'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])

            ->addColumn('prihlasky_pocet', 'smallinteger', ['null' => true, 'comment' => 'Pocet prihlasek'])
            ->addColumn('pohledavky_pocet', 'smallinteger', ['null' => true, 'comment' => 'Pocet pohledavek'])
            ->addColumn('pocet_nezajistenych', 'smallinteger', ['null' => true, 'comment' => 'Pocet nz. pohledavek'])
            ->addColumn('pocet_zajistenych', 'smallinteger', ['null' => true, 'comment' => 'Pocet zaj. pohledavek'])

            ->addColumn('pocet_splatna', 'smallinteger', ['null' => true])
            ->addColumn('pocet_podrizena', 'smallinteger', ['null' => true])
            ->addColumn('pocet_vykonatelna', 'smallinteger', ['null' => true])
            ->addColumn('pocet_v_cizi_mene', 'smallinteger', ['null' => true])
            ->addColumn('pocet_penezita', 'smallinteger', ['null' => true])
            
            ->addColumn('celkova_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Celkova prihlasena castka (z+n)'])
            ->addColumn('celkova_vyse_nezajistenych', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('celkova_vyse_zajistenych', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])

            ->addColumn('celkova_vyse', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vykonatelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('nevykonatelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('duplicitni', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('neprezkoumavano', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('odmitnuto', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('podmineno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('popreno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('zbyva_uspokojit', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('zjisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])

            ->addForeignKey('spisovaznacka', 'isir_vec', 'spisovaznacka', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['spisovaznacka'], ['unique' => true])

            ->create();

    }
}
