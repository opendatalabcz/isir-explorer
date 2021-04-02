<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class DataKraje extends AbstractMigration
{
    public function up(): void
    {
        $singleRow = [
            'nazev'    => 'data.csu.kraje.obyvatele',
            'rok'  => 2020,
            'data' => '{"OL": 632015, "KR": 551647, "JC": 644083, "LI": 443690, "PL": 589899, "PR": 1324277, "ZL": 582555, "ST": 1385141, "JM": 1191989, "MO": 1200539, "KA": 294664, "US": 820965, "VY": 509813, "PA": 522662}'
        ];

        $table = $this->table('statistiky');
        $table->insert($singleRow);
        $table->saveData(); 
    }

    public function down()
    {
    }
}
