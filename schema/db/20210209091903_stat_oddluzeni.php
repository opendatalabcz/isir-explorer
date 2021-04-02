<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class StatOddluzeni extends AbstractMigration
{
    public function change(): void
    {

        $table = $this->table('stat_oddluzeni', [
            'comment' => 'Statistiky pro rizeni resene oddluzenim'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])

            ->addColumn('zpro_id', 'integer', ['null' => true, 'comment' => 'Odkaz na aktualni zpravu pro oddluzeni pro toto rizeni'])
            ->addColumn('zspo_id', 'integer', ['null' => true, 'comment' => 'Odkaz na aktualni zpravu o splneni oddluzeni pro toto rizeni'])

            ->addColumn('vysledek_oddluzeni', 'boolean', ['null' => true, 'comment' => 'True=Priznani osvobozeni od pohledavek, False=Zruseni oddluzeni'])

            ->addColumn('n_osvobozeno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Vyse zavazku nezaj. ver. od kterych byl dl. osvobozen'])
            ->addColumn('z_osvobozeno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Vyse zavazku zaj. ver. od kterych byl dl. osvobozen'])

            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addForeignKey('zspo_id', 'zprava_splneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addForeignKey('spisovaznacka', 'isir_vec', 'spisovaznacka', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['spisovaznacka'], ['unique' => true])

            ->create();

    }
}
