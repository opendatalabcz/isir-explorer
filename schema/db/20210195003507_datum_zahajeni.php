<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class DatumZahajeni extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('isir_vec');
        $table->addColumn('datumzahajeni', 'timestamp', ['null'=>true, 'comment' => 'Datum zahajeni rizeni'])
              ->update();
    }
}
