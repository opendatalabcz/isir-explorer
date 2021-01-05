<?php

declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class Isir extends AbstractMigration
{
    public function change(): void
    {
        $table = $this->table('isir_udalost', [
            'id' => false,
            'primary_key' => ['spisovaznacka', 'oddil', 'cislovoddilu', 'typudalosti'],
            'comment' => 'Udalosti a prislusne dokumenty zverejnene v insolvencnim rejstriku (zdroj: isir-ws)'
        ]);
        $table->addColumn('id', 'integer', ['null' => false])
            ->addColumn('soud', 'smallinteger', ['null' => true])
            ->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])
            ->addColumn('oddil', 'string', ['null' => false, 'limit' => 10])
            ->addColumn('cislovoddilu', 'smallinteger', ['null' => false])
            ->addColumn('typudalosti', 'smallinteger', ['null' => false, 'comment' => 'Typ udalosti dle ciselniku udalosti ISIR'])
            ->addColumn('dokumenturl', 'string', ['null' => true, 'limit' => 100, 'comment' => 'Identifikator, pod kterym lze stahnout PDF dokument z webu ISIRu'])
            ->addColumn('datumzalozeniudalosti', 'timestamp', ['null' => true])
            ->addColumn('datumzverejneniudalosti', 'timestamp', ['null' => true])
            ->addColumn('poznamka_json', 'text', ['null' => true, 'comment' => 'Dodatecne informace k udalosti'])
            ->addColumn('priznakanvedlejsiudalost', 'boolean', ['null' => true, 'comment' => 'Priznak, zda jde o vedlejsi udalost (dokument je u hlavni udalosti)'])
            ->addColumn('priznakanvedlejsidokument', 'boolean', ['null' => true, 'comment' => 'Priznak, zda jde o vedlejsi dokument'])
            ->addColumn('priznakplatnyveritel', 'boolean', ['null' => true])
            ->addColumn('priznakmylnyzapisveritelpohled', 'boolean', ['null' => true])
            ->addColumn('stav', 'smallinteger', ['null' => true, 'comment' => 'Stav rizeni v dobe zalozeni teto udalost'])
            ->addColumn('pocet_zmen', 'smallinteger', ['null' => true, 'default' => 0, 'comment' => 'Kolikrat byla tato udalost v rejstriku aktualizovana'])
            ->addColumn('dl_precteno', 'timestamp', ['null' => true, 'comment' => 'Datum scrapovani asociovaneho PDF dokumentu'])
            ->addIndex(['id'], ['unique' => true])
            ->addIndex(['spisovaznacka', 'oddil', 'cislovoddilu', 'typudalosti'], ['unique' => true])
            ->create();

        $table = $this->table('isir_osoba', [
            'comment' => 'Subjekty evidovane v insolvencnim rejstriku (zdroj: isir-ws)'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])
            ->addColumn('idosoby', 'string', ['null' => false, 'comment' => 'Identifikator prirazeny webovou sluzbou MSp'])
            ->addColumn('soud', 'smallinteger', ['null' => true, 'comment' => 'Prislusnost osoby ke kraji/soudu podle rizeni, dle ciselniku webservice.enums'])
            ->addColumn('druhrolevrizeni', 'smallinteger', ['null' => true, 'comment' => '1=dluznik, 2=spravce, 3=veritel, 4=veritel-navr, dle viz webservice.enums'])
            ->addColumn('druhspravce', 'smallinteger', ['null' => true, 'comment' => 'Typ spravce dle ciselniku webservice.enums'])
            ->addColumn('nazevosoby', 'string', ['null' => true, 'limit' => 255, 'comment' => 'Prijmeni fyzicke osoby nebo nazev pravnicke osoby'])
            ->addColumn('nazevosobyobchodni', 'string', ['null' => true, 'limit' => 255, 'comment' => 'Obchodni nazev osoby'])
            ->addColumn('druhosoby', 'smallinteger', ['null' => true, 'comment' => '1=fyzicka, 2=organizace_resortu, 3=pravnicka, 4=spravce, ..., dale viz webservice.enums'])
            ->addColumn('druhpravniforma', 'smallinteger', ['null' => true, 'comment' => 'Typ pravni formy osoby dle ciselniku webservice.enums'])
            ->addColumn('jmeno', 'string', ['null' => true, 'limit' => 255, 'comment' => 'Jmeno fyzicke osoby pokud jde o fyzickou osobu'])
            ->addColumn('titulpred', 'string', ['null' => true, 'limit' => 50, 'comment' => 'Titul fyzicke osoby pokud jde o fyzickou osobu'])
            ->addColumn('titulza', 'string', ['null' => true, 'limit' => 50, 'comment' => 'Titul fyzicke osoby pokud jde o fyzickou osobu'])
            ->addColumn('ic', 'string', ['null' => true, 'limit' => 9, 'comment' => 'Identifikacni cislo (pravnicka osoba nebo fyz. osoba podnikatel)'])
            ->addColumn('dic', 'string', ['null' => true, 'limit' => 14, 'comment' => 'DIC, je-li evidovano'])
            ->addColumn('rc', 'string', ['null' => true, 'limit' => 11, 'comment' => 'Rodne cislo fyzicke osoby'])
            ->addColumn('datumosobavevecizrusena', 'timestamp', ['null' => true, 'comment' => 'Od jakeho data neposkytovat informace o osobe'])
            ->addColumn('datumnarozeni', 'date', ['null' => true, 'comment' => 'Datum narozeni fyzicke osoby'])
            ->addColumn('datumzalozeni', 'timestamp', ['null' => true, 'comment' => 'Datum prvniho vlozeni zaznamu teto osoby do ins. rejstriku'])
            ->addColumn('idzalozeni', 'integer', ['null' => true, 'comment' => 'Id udalosti (isir_udalost), ktera zalozila tuto osobu'])
            ->addColumn('pocet_zmen', 'smallinteger', ['null' => true, 'default' => 0, 'comment' => 'Kolikrat byl zaznam teto osoby v rejstriku zmenen'])
            ->addColumn('cislo_veritele', 'smallinteger', ['null' => true, 'comment' => 'Pokud jde o veritele, cislo veritele v tomto rizeni - nejde o hodnotu z API, je doplnena dle prehledoveho listu'])

            ->addIndex(['ic'], ['unique' => false])
            ->addIndex(['rc'], ['unique' => false])
            ->addIndex(['spisovaznacka', 'idosoby'], ['unique' => true])
            ->addIndex(['nazevosoby', 'jmeno', 'datumnarozeni'], ['unique' => false])

            ->create();

        $table = $this->table('isir_vec', [
            'id' => false,
            'primary_key' => ['spisovaznacka'],
            'comment' => 'Seznam insolvencnich rizeni evidovanych v insolvencnim rejstriku (zdroj: isir-ws)'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])
            ->addColumn('druhstavrizeni', 'smallinteger', ['null' => false])
            ->addColumn('datumveczrusena', 'string', ['null' => true])
            ->addColumn('datumkoneclhutyprihlasek', 'timestamp', ['null' => true])
            ->addColumn('datumskonceniveci', 'timestamp', ['null' => true])
            ->addColumn('datumaktualizace', 'timestamp', ['null' => true])
            ->addColumn('pocet_zmen', 'smallinteger', ['null' => false, 'default' => 0])
            ->create();

        $table = $this->table('isir_vec_stav', [
            'comment' => 'Stavy rizeni u jednotlivych insolvencnich rizeni (zdroj: isir-ws)'
        ]);
        $table->addColumn('spisovaznacka', 'string', ['null' => false, 'limit' => 50])
            ->addColumn('druhstavrizeni', 'smallinteger', ['null' => false])
            ->addColumn('datum', 'timestamp', ['null' => false])
            ->addColumn('rid', 'integer', ['null' => true])
            ->addIndex(['spisovaznacka'], ['unique' => false])
            ->create();
    }
}
