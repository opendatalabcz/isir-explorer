<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class MesicOddluzeniNull extends AbstractMigration
{
    public function up(): void
    {

        // Povoleni NULL ve sloupci mesic ve vykazu oddluzeni, protoze u mnoha formularu tato informace neni vyplnena

        $table = $this->table('zplo_vykaz_plneni');
        $table->changeColumn('mesic', 'smallinteger', ['null' => true])
               ->changeColumn('mesic_oddluzeni', 'smallinteger', ['null' => true])
               ->save();
    }

    /**
     * Migrate Down.
     */
    public function down()
    {
        $table = $this->table('zplo_vykaz_plneni');
        $table->changeColumn('mesic', 'smallinteger', ['null' => false])
               ->changeColumn('mesic_oddluzeni', 'smallinteger', ['null' => false])
               ->save();
    }
}
