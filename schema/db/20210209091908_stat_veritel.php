<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class StatVeritel extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('stat_veritel', [
            'comment' => 'Seznam věřitelů'
        ]);
        $table->addColumn('ic', 'string', ['null' => true, 'limit' => 9, 'comment' => 'Identifikacni cislo (pravnicka osoba nebo fyz. osoba podnikatel)'])
            ->addColumn('nazev', 'string', ['null' => false, 'comment' => 'Plne jmeno (s tituly) nebo obchodni nazev'])
            ->addColumn('jmeno', 'string', ['null' => true, 'comment' => 'Jmeno, pokud nejde o pravnickou osobu'])
            ->addColumn('prijmeni', 'string', ['null' => true, 'comment' => 'Prijmeni, pokud nejde o pravnickou osobu'])
            ->addColumn('ins_celkem', 'integer', ['null' => true, 'comment' => 'Pocet rizenich v jakych veritel figuruje'])
            ->addColumn('prihlasky_pocet', 'integer', ['null' => true, 'comment' => 'Pocet prihlasek (pouze prectene)'])
            ->addColumn('pohledavky_pocet', 'integer', ['null' => true, 'comment' => 'Pocet pohledavek'])
            ->addColumn('vyse_celkem', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Celkova vyse prihlasenych'])
            ->addColumn('vyse_nezaj', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Celkova vyse prihlasenych nezajistenych'])
            ->addColumn('vyse_zaj', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC, 'comment' => 'Celkova vyse prihlasenych zajistenych'])
            ->addIndex(['ic'], ['unique' => false])
            ->create();

        // ----------------------------------------------------------------------

        $table = $this->table('stat_veritel_ins', [
            'comment' => 'Vazby mezi veriteli a jejich rizenimi',
            'id' => false,
            'primary_key' => ['id_veritel', 'id_ins'],
        ]);

        $table->addColumn('id_veritel', 'integer', ['null' => false])
            ->addColumn('id_ins', 'integer', ['null' => false])

            ->addForeignKey('id_veritel', 'stat_veritel', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addForeignKey('id_ins', 'stat_vec', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])

            ->create();
    }
}
