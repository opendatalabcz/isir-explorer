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

               ->changeColumn('prijem', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('srazky', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('zm_nnb', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('nepostizitelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('postizitelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('vraceno_dluznikum', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('mimoradny_prijem', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('darovaci_smlouva', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('odmena_is', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('vyzivne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('ostatnim_veritelum', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])

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

               ->changeColumn('prijem', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('srazky', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('zm_nnb', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('nepostizitelne', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('postizitelne', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('vraceno_dluznikum', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('mimoradny_prijem', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('darovaci_smlouva', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('odmena_is', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('vyzivne', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
               ->changeColumn('ostatnim_veritelum', 'decimal', ['null' => false, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])

               ->save();
    }
}
