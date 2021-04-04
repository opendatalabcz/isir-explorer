<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class StatVec2 extends AbstractMigration
{
    public function change(): void
    {

        $table = $this->table('stat_vec');
        $table
            ->addColumn('zahajeni_r', 'smallinteger', ['null' => true, 'comment' => 'Rok zahajeni' ])
            ->addColumn('zahajeni_m', 'smallinteger', ['null' => true, 'comment' => 'Mesic zahajeni' ])
            ->addColumn('ukonceni_r', 'smallinteger', ['null' => true, 'comment' => 'Rok ukonceni' ])
            ->addColumn('ukonceni_m', 'smallinteger', ['null' => true, 'comment' => 'Mesic ukonceni' ])
            ->addIndex(['zahajeni_r', 'zahajeni_m'], ['unique' => false])
            ->addIndex(['ukonceni_r', 'ukonceni_m'], ['unique' => false])
            ->save();

    }
}
