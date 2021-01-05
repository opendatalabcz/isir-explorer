<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class DlStats extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('dl_stats', ['comment' => 'Informace o stazenych a importovanych dokumentech programem isir-dl']);
        $table
            ->addColumn('tstart', 'timestamp', ['null' => false, 'comment' => 'Cas spusteni stahovani'])
            ->addColumn('tend', 'timestamp', ['null' => false, 'comment' => 'Cas ukonceni stahovani'])
            ->addColumn('seconds', 'integer', ['null' => false, 'comment' => 'Doba behu v sekundach'])
            ->addColumn('mib', 'decimal', ['null' => true, 'scale' => 3, 'precision' => 10, 'comment' => 'Datovy objem stazenych dat tohoto behu programu'])
            ->addColumn('docs', 'integer', ['null' => true, 'comment' => 'Pocet stazenych pdf souboru'])
            ->addColumn('not_empty', 'integer', ['null' => true, 'comment' => 'Pocet neprazdnych pdf souboru (vyrazeny doruc. dolozky atp.)'])
            ->addColumn('readable', 'integer', ['null' => true, 'comment' => 'Pocet pdf souboru citelnych programem isir-scraper'])
            ->addColumn('imported', 'integer', ['null' => true, 'comment' => 'Pocet importovanych dokumentu (jedno pdf muze mit vice formularu)'])
            ->addColumn('errors', 'integer', ['null' => true, 'comment' => 'Kolik nastalo chyb pri importu'])
            ->create();
    }
}
