<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class OsobaSpojena extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('pp_osoba');
        $table->addColumn('osoba_spojena', 'smallinteger', ['null'=>true, 'comment' => 'Stav prirazeni tohoto zaznamu k osobe (isir_osoba)'])
              ->update();

        $table = $this->table('pl_pohledavka');
        $table->addColumn('osoba_spojena', 'smallinteger', ['null'=>true, 'comment' => 'Stav prirazeni tohoto zaznamu k osobe (isir_osoba)'])
            ->update();

        $table = $this->table('zpro_distribucni_schema');
        $table->addColumn('osoba_spojena', 'smallinteger', ['null'=>true, 'comment' => 'Stav prirazeni tohoto zaznamu k osobe (isir_osoba)'])
                ->update();

        $table = $this->table('zplo_vykaz_prerozdeleni_veritel');
        $table->addColumn('osoba_spojena', 'smallinteger', ['null'=>true, 'comment' => 'Stav prirazeni tohoto zaznamu k osobe (isir_osoba)'])
                ->update();
    }
}
