<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class Statistiky extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('statistiky', [
            'comment' => 'Agregovaná statistická data určená pro zobrazení v grafech'
        ]);
        $table->addColumn('nazev', 'string', ['null' => false, 'limit' => 100, 'comment' => 'Označení dat'])
            ->addColumn('rok', 'string', ['null' => true, 'comment' => 'Rok, pro který jsou data platná, nebo null pokud nemají časové vymezení'])
            ->addColumn('mesic', 'integer', ['null' => true, 'comment' => 'Mesic, pro který jsou data platná, nebo null pokud nemají časové vymezení'])
            ->addColumn('data', 'text', ['null' => false, 'comment' => 'JSON s daty'])
            ->addColumn('created_at', 'timestamp', ['null' => false, 'default' => 'CURRENT_TIMESTAMP', 'comment' => 'Datum vytvoření'])
            ->addColumn('updated_at', 'timestamp', ['null' => false, 'default' => 'CURRENT_TIMESTAMP', 'update' => 'CURRENT_TIMESTAMP', 'comment' => 'Datum aktualizace'])
            ->addIndex(['nazev'], ['unique' => false])
            ->create();
    }
}
