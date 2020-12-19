<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class IsirCisUdalosti extends AbstractMigration
{

    const DATA_FILE = '20201219095027_isir_cis_udalosti.csv';

    /**
     * Precte csv soubor do asociativniho pole, zaznamy maji klice dle hlavicky csv souboru
     */
    protected function readCSV($file)
    {
        $csv = array_map('str_getcsv', file($file));
        array_walk($csv, function (&$a) use ($csv) {
            $a = array_combine($csv[0], $a);
        });
        array_shift($csv);
        return $csv;
    }
    
    public function up(): void
    {
        $table = $this->table('isir_cis_udalosti', [
            'id' => false,
            'primary_key' => ['id'],
            'comment' => 'Ciselnik typu udalost v insolvencnim rejstriku (zdroj: dokumentace isir-ws)'
        ]);
        $table->addColumn('id', 'smallinteger', ['null' => false])
            ->addColumn('nazev', 'string', ['null' => false, 'limit' => 255])
            ->addColumn('je_servisni', 'boolean', ['null' => true, 'comment' => 'Priznak, zda jde o servisni udalost (skryta udalost bez zverejneneho dokumentu)'])
            ->addColumn('je_citelna', 'boolean', ['null' => true, 'comment' => 'Priznak, zda je pdf formular zverejnovany s touto udalosti citelny parserem nastroje isir-scraper'])
            ->create();
        $this->table('isir_cis_udalosti')
            ->insert($this->readCSV(__DIR__ . '/data/' . self::DATA_FILE))
            ->save();
    }

    public function down(): void
    {
        $this->table('isir_cis_udalosti')->drop()->save();
    }
}
