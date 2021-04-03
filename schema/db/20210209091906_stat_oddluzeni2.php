<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class StatOddluzeni2 extends AbstractMigration
{
    public function change(): void
    {

        $table = $this->table('stat_oddluzeni');
        $table
            ->addColumn('n_uspokojeni_mira', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Uspokojeni nezajistenych veritelu mira'])
            ->addColumn('z_uspokojeni_mira', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Uspokojeni zajistenych veritelu mira'])

            ->addColumn('n_uspokojeni_vs_predpoklad', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Rozdil usp. nez. oproti predpokladu uspokojeni (= mira - predpolad)' ])
            ->addColumn('n_uspokojeni_predpoklad', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Predpoklad usp. nez.' ])
            
            ->addColumn('delka_oddluzeni', 'smallinteger', ['null' => true, 'comment' => 'Rozdil hodnot posledni_splatka a oddluzeni_schvaleno' ])
            ->addColumn('delka_zjis_upadku', 'smallinteger', ['null' => true, 'comment' => 'Rozdil hodnot zahajeno a zjisteni_upadku' ])
            ->addColumn('delka_schvalovani', 'smallinteger', ['null' => true, 'comment' => 'Rozdil hodnot oddluzeni_povoleno a oddluzeni_schvaleno' ])
            ->addColumn('delka_pred_schvalenim', 'smallinteger', ['null' => true, 'comment' => 'Rozdil hodnot oddluzeni_povoleno a oddluzeni_schvaleno' ])
            ->save();

    }
}
