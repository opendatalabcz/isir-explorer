<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class DokumentZverejneni extends AbstractMigration
{
    public function change(): void
    {

        $table = $this->table('dokument');
        $table
            ->addColumn('zverejneni', 'timestamp', ['null' => true, 'comment' => 'Datum zverejneni dokumentu v rejstriku'])
            ->save();

    }
}
