<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class VlastnostiPohledavky extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('pp_pohledavka');
        $table->addColumn('v_cizi_mene', 'boolean', ['null'=>false, 'comment' => 'Pohledávka je v cizí měně'])
              ->addColumn('penezita', 'boolean', ['null'=>false, 'comment' => 'Pohledávka je penezita'])
              ->update();
    }
}
