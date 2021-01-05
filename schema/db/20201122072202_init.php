<?php
declare(strict_types=1);

// Daotvy typ MONEY se casto definuje jako DECIMAL(16,2)
define("DEC_SCAL", 2);
define("DEC_PREC", 16);

use Phinx\Migration\AbstractMigration;

final class Init extends AbstractMigration
{
    public function change(): void
    {

      $table = $this->table('dokument', ['comment' => 'Asociace pdf dokumentu z ISIRu k prectenemu dokumentu']);
      $table->addColumn('isir_id', 'string', ['null' => true, 'limit' => 100, 'comment' => 'ID dokumentu v ISIRu (dokumenturl)'])
          ->addColumn('spisova_znacka', 'string', ['null' => false, 'limit' => 50])
          ->addColumn('typ', 'smallinteger', ['null' => false, 'comment' => 'Typ parseru'])
          ->addColumn('verze_dokument', 'string', ['null' => true, 'limit' => 10, 'comment' => 'Oznaceni verze pdf dokumentu (je-li dostupne)'])
          ->addColumn('verze_scraper', 'smallinteger', ['null' => true, 'comment' => 'Verze scraperu (pro dany typ dokumentu), ktery byl pouzit pro precteni'])
          ->addColumn('datum', 'timestamp', ['null' => false, 'comment' => 'Datum precteni dokumentu'])
          ->addIndex(['isir_id'], ['unique' => false])
          ->addIndex(['spisova_znacka'], ['unique' => false])
          ->addForeignKey('spisova_znacka', 'isir_vec', 'spisovaznacka', ['delete'=> 'CASCADE', 'update'=> 'RESTRICT'])
          ->create();

        /* ====================================================================================== */
        /* ============ Prihlaska pohledavky ============ */

        $table = $this->table('prihlaska_pohledavky', ['id' => false, 'primary_key' => ['id'], 'comment' => 'Dokument - Prihlaska pohledavky (z pdf)']);
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('cislo_prihlasky', 'integer', ['null' => true, 'comment' => 'Cislo prihlasky pohledavky v ins. rizeni (dle cisla v oddilu P)'])
              ->addColumn('pocet_pohledavek', 'integer')
              ->addColumn('celkova_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('celkova_vyse_nezajistenych', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('celkova_vyse_zajistenych', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('id', 'dokument', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

      $table = $this->table('pp_osoba', ['comment' => 'Osoba v prihlasce pohledavky (zejmena veritel)']);
      $table->addColumn('pp_id', 'integer', ['comment' => 'Prihlaska pohledavky'])
              ->addColumn('druhrolevrizeni', 'smallinteger', ['null' => false, 'comment' => '1=dluznik, 2=spravce, 3=veritel, 4=veritel-navr, dle webservice.enums'])
              ->addColumn('nazevosoby', 'string', ['null' => true, 'limit' => 255, 'comment' => 'Prijmeni fyzicke osoby nebo nazev pravnicke osoby'])
              ->addColumn('druhosoby', 'smallinteger', ['null' => true, 'comment' => '1=fyzicka, 2=organizace_resortu, 3=pravnicka, 4=spravce, ..., viz webservice.enums'])
              ->addColumn('jmeno', 'string', ['null' => true, 'limit' => 255, 'comment' => 'Jmeno fyzicke osoby pokud jde o fyzickou osobu'])
              ->addColumn('titulpred', 'string', ['null' => true, 'limit' => 50, 'comment' => 'Titul fyzicke osoby pokud jde o fyzickou osobu'])
              ->addColumn('titulza', 'string', ['null' => true, 'limit' => 50, 'comment' => 'Titul fyzicke osoby pokud jde o fyzickou osobu'])
              ->addColumn('ic', 'string', ['null' => true, 'limit' => 9, 'comment' => 'Identifikacni cislo (pravnicka osoba nebo fyz. osoba podnikatel)'])
              ->addColumn('rc', 'string', ['null' => true, 'limit' => 11, 'comment' => 'Rodne cislo fyzicke osoby'])
              ->addColumn('reg_cislo', 'string', ['null' => true, 'limit' => 255, 'comment' => 'Jine registracni cislo (napr. pro zahranicni subjekty)'])
              ->addColumn('datumnarozeni', 'date', ['null' => true, 'comment' => 'Datum narozeni fyzicke osoby'])
              ->addColumn('cislo_uctu', 'string', ['null' => true, 'limit' => 255])
              ->addColumn('isir_osoba', 'integer', ['null' => true, 'comment' => 'Asociace isir_osoba, je doplneno dle dostupnych udaju o osobe a nemusi byt vzdy presne'])
              ->addForeignKey('pp_id', 'prihlaska_pohledavky', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addForeignKey('isir_osoba', 'isir_osoba', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['pp_id'], ['unique' => false])
              ->addIndex(['isir_osoba'], ['unique' => false])
              ->create();

      $table = $this->table('pp_osoba_sidlo', ['comment' => 'Adresa sidla osoby dle udaju v prihlasce']);
      $table->addColumn('osoba_id', 'integer', ['comment' => 'Id osoby v prihlasce (pp_osoba.id)'])
              ->addColumn('ulice', 'string', ['null' => true])
              ->addColumn('cp', 'string', ['null' => true, 'limit' => 10])
              ->addColumn('co', 'string', ['null' => true, 'limit' => 10])
              ->addColumn('obec', 'string', ['null' => true, 'limit' => 255])
              ->addColumn('psc', 'string', ['null' => true, 'limit' => 10])
              ->addColumn('cast_obce', 'string', ['null' => true, 'limit' => 255])
              ->addColumn('stat', 'string', ['null' => true, 'limit' => 255])
              ->addForeignKey('osoba_id', 'pp_osoba', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['osoba_id'], ['unique' => false])
              ->create();

        $table = $this->table('pp_pohledavka', ['comment' => 'Pohledavka v prihlasce']);
        $table->addColumn('pp_id', 'integer', ['comment' => 'Prihlaska pohledavky'])
              ->addColumn('cislo', 'integer', ['comment' => 'Cislo pohledavky v ramci prihlasky pohledavky'])
              ->addColumn('celkova_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('vyse_jistiny', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC, 'null' => true])
              ->addColumn('typ', 'smallinteger', ['null' => true, 'comment' => 'Typ pohledavky (z textu preveden na cis. hodnotu dle enum PrihlaskaImporter)'])
              ->addColumn('typ_text', 'string', ['null' => true, 'limit' => 50, 'comment' => 'Textove vyjadreni typu jak je uvedeno v dokumentu'])
              ->addColumn('dalsi_okolnosti', 'text', ['null' => true])
              ->addColumn('duvod_vzniku', 'text', ['null' => true])
              ->addColumn('splatna', 'boolean')
              ->addColumn('podrizena', 'boolean')
              ->addColumn('vykonatelnost', 'boolean')
              ->addForeignKey('pp_id', 'prihlaska_pohledavky', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['pp_id'], ['unique' => false])
              ->create();
        // TODO detail splatnosti, prislusenstvi, vykonatelnost, podrizenost

        /* ====================================================================================== */
        /* ============ Prehledovy list ============ */

        $table = $this->table('prehledovy_list', ['id' => false, 'primary_key' => ['id'], 'comment' => 'Dokument - Prehledovy list - souhrn pro nezajistene a zajistene veritele (z pdf)']);
              // Nezajisteni veritele
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('n_celkova_vyse', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_vykonatelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_nevykonatelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_duplicitni', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_neprezkoumavano', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_odmitnuto', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_podmineno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_popreno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_zbyva_uspokojit', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_zjisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              // Zajisteni veritele
              ->addColumn('z_celkova_vyse', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_vykonatelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_nevykonatelne', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_duplicitni', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_neprezkoumavano', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_odmitnuto', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_podmineno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_popreno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_zbyva_uspokojit', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_zjisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('id', 'dokument', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('pl_pohledavka', ['comment' => 'Pohledavka v prehledovem listu']);
        $table->addColumn('pl_id', 'integer')
              ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
              ->addColumn('celkova_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('cislo_prihlasky', 'smallinteger')
              ->addColumn('cislo_veritele', 'smallinteger')
              ->addColumn('datum_doruceni', 'date', ['null' => true])
              ->addColumn('duplicitni', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('neprezkoumavano', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('nevykonatelne', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('odmitnuto', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('podmineno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('popreno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('procent', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('veritel', 'text', ['comment' => 'Textova identifikace veritele, jak je uvedena ve formulari', 'null' => true])
              ->addColumn('veritel_id', 'integer', ['comment' => 'Asociace veritele na isir_osoba, je doplneno dle cisla veritele a nemusi byt vzdy presne', 'null' => true])
              ->addColumn('vykonatelne', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('zbyva_uspokojit', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('zjisteno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('pl_id', 'prehledovy_list', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addForeignKey('veritel_id', 'isir_osoba', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['pl_id'], ['unique' => false])
              ->addIndex(['veritel_id'], ['unique' => false])
              ->create();

        /* ====================================================================================== */
        /* ============ Zprava pro oddluzeni ============ */

        $table = $this->table('zprava_pro_oddluzeni', ['id' => false, 'primary_key' => ['id'], 'comment' => 'Dokument - Zprava pro oddluzeni (z pdf)']);
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('odmena_za_sepsani_navrhu', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('povinnen_vydat_obydli', 'string', ['null' => true])
              ->addColumn('vyse_zalohy', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('vytezek_zpenezeni_obydli', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('zpracovatel_navrhu', 'string', ['null' => true])
              ->addColumn('prijmy_celkem', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('prijmy_komentar', 'text', ['null' => true])

              ->addColumn('celkem_majetek_oceneni', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('celkem_majetek_nezajisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('celkem_majetek_zajisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              
              ->addColumn('okolnosti_proti_oddluzeni', 'text', ['null' => true])
              ->addColumn('navrh_dluznika', 'text', ['null' => true])
              ->addColumn('navrh_spravce', 'text', ['null' => true])
              ->addForeignKey('id', 'dokument', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('zpro_soupis_majetku', ['comment' => 'Soupis majetku dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ_majetku', 'smallinteger')
            ->addColumn('oceneni', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('nezajisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('zajisteno', 'decimal', ['null' => true, 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['zpro_id'], ['unique' => false])
            ->create();

        $table = $this->table('zpro_prijem_dluznika', ['comment' => 'Prijem dluznika dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('nazev_platce', 'string', ['null' => true])
            ->addColumn('adresa', 'string', ['null' => true])
            ->addColumn('ico', 'string', ['limit' => 60, 'null' => true])
            ->addColumn('typ', 'string', ['null' => true])
            ->addColumn('vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['zpro_id'], ['unique' => false])
            ->create();

        $table = $this->table('zpro_distribucni_schema', ['comment' => 'Distribucni schema dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
            ->addColumn('veritel', 'integer', ['comment' => 'Cislo veritele, jak je uvedeno v dokumentu'])
            ->addColumn('veritel_id', 'integer', ['comment' => 'Asociace veritele na isir_osoba, je doplneno dle cisla veritele a nemusi byt vzdy presne', 'null' => true])
            ->addColumn('castka', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('podil', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addForeignKey('veritel_id', 'isir_osoba', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['zpro_id'], ['unique' => false])
            ->addIndex(['veritel_id'], ['unique' => false])
            ->create();

        $table = $this->table('zpro_predpoklad_uspokojeni', ['comment' => 'Predpoklad uspokojeni dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
            ->addColumn('uspokojeni', 'smallinteger', ['comment' => 'Typ uspokojeni'])
            ->addColumn('mira', 'decimal', ['comment' => 'Procent', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vyse', 'decimal', ['comment' => 'Castka v Kc', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['zpro_id'], ['unique' => false])
            ->create();

        /* ====================================================================================== */
        /* ============ Zprava o plneni oddluzeni ============ */

        $table = $this->table('zprava_plneni_oddluzeni', ['id' => false, 'primary_key' => ['id'], 'comment' => 'Dokument - Zprava o plneni oddluzeni (z pdf)']);
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('doporuceni_spravce', 'text')
              ->addColumn('doporuceni_spravce_oduvodneni', 'text')
              ->addColumn('duvod_neplneni', 'text')
              ->addColumn('plni_povinnosti', 'string')
              ->addColumn('stanovisko_dluznika', 'text')
              ->addColumn('vyjadreni_spravce', 'text')

              ->addColumn('n_uspokojeni_ocekavana', 'decimal', ['null' => true, 'comment' => 'Ocekavana mira uspokojeni nezajistenych pohledavek', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_uspokojeni_aktualni', 'decimal' , ['null' => true, 'comment' => 'Aktualni mira uspokojeni nezajistenych pohledavek', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_uspokojeni_ocekavana', 'decimal', ['null' => true, 'comment' => 'Ocekavana mira uspokojeni zajistenych pohledavek', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_uspokojeni_aktualni', 'decimal',  ['null' => true, 'comment' => 'Aktualni mira uspokojeni zajistenych pohledavek', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('id', 'dokument', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('zplo_vykaz_plneni', ['comment' => 'Vykaz plneni oddluzeni po jednotlivych mesicich']);
        $table->addColumn('zplo_id', 'integer', ['comment' => 'Zprava o plneni oddluzeni'])
              ->addColumn('rok', 'smallinteger')
              ->addColumn('mesic', 'smallinteger')
              ->addColumn('mesic_oddluzeni', 'smallinteger')
              ->addColumn('prijem', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('srazky', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('zm_nnb', 'decimal', ['comment' => 'Zivotni minimum + Normovane naklady na bydleni', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])

              ->addColumn('vyzivovane_osoby', 'smallinteger')
              ->addColumn('nepostizitelne', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('postizitelne', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('vraceno_dluznikum', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('mimoradny_prijem', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('darovaci_smlouva', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('k_prerozdeleni', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('odmena_is', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('vyzivne', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('ostatnim_veritelum', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])

              ->addColumn('celkem_prerozdeleno', 'decimal', ['comment' => 'Kc doposud rozdeleno veritelum k tomuto mesici', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('mira_uspokojeni', 'decimal', ['comment' => 'Aktualni mira uspokojeni k tomuto mesici', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('mira_uspkojeni_ocekavana', 'decimal', ['comment' => 'Ocekavana mira uspokojeni k tomuto mesici', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])

              ->addForeignKey('zplo_id', 'zprava_plneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['zplo_id'], ['unique' => false])
              ->create();

        $table = $this->table('zplo_vykaz_prerozdeleni_veritel', ['comment' => 'Vykaz prerozdeleni pro jednotlive veritele']);
        $table->addColumn('zplo_id', 'integer', ['comment' => 'Zprava o plneni oddluzeni'])
              ->addColumn('veritel', 'string', ['comment' => 'Textove oznaceni veritele, tak jak je to uvedeno v dokumentu'])
              ->addColumn('veritel_id', 'integer', ['comment' => 'Asociace veritele na isir_osoba, je doplneno dle textoveho popisu a nemusi byt vzdy presne', 'null' => true])
              ->addColumn('castka', 'decimal', ['comment' => 'Celkova dluzna castka', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('podil', 'decimal', ['comment' => 'Podil veritele na distr. schematu', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('zplo_id', 'zprava_plneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addForeignKey('veritel_id', 'isir_osoba', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['zplo_id'], ['unique' => false])
              ->addIndex(['veritel_id'], ['unique' => false])
              ->create();

        $table = $this->table('zplo_vykaz_prerozdeleni', ['comment' => 'Vykaz prerozdeleni po jednotlivych mesicich pro jednotlive veritele']);
        $table->addColumn('zplo_veritel_id', 'integer', ['comment' => 'Veritel ve vykazu prerozdeleni'])
              ->addColumn('rok', 'smallinteger')
              ->addColumn('mesic', 'smallinteger')
              ->addColumn('mesic_oddluzeni', 'smallinteger')

              ->addColumn('vyplaceno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('zplo_veritel_id', 'zplo_vykaz_prerozdeleni_veritel', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->addIndex(['zplo_veritel_id'], ['unique' => false])
              ->create();

        /* ====================================================================================== */
        /* ============ Zprava o splneni oddluzeni ============ */

        $table = $this->table('zprava_splneni_oddluzeni', ['id' => false, 'primary_key' => ['id'], 'comment' => 'Dokument - Zprava o splneni oddluzeni (z pdf)']);
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('oddluzeni_povoleno', 'date', ['null' => true])
              ->addColumn('oddluzeni_schvaleno', 'date', ['null' => true])
              ->addColumn('zahajeno', 'date', ['null' => true])
              ->addColumn('zjisteni_upadku', 'date', ['null' => true])
              ->addColumn('posledni_splatka', 'date', ['null' => true])
              ->addColumn('zaslani_vyzvy_ukonceni_srazek', 'date', ['null' => true])

              ->addColumn('doporuceni_spravce', 'text')
              ->addColumn('doporuceni_spravce_oduvodneni', 'text')
              ->addColumn('zprava_o_prubehu', 'text')

              ->addColumn('n_predpoklad_uspokojeni_mira', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_predpoklad_uspokojeni_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_uspokojeni_mira', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('n_uspokojeni_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_uspokojeni_mira', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('z_uspokojeni_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('preplatek', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('id', 'dokument', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('zspo_odmena_spravce', ['comment' => 'Informace o odmene ins. spravce dle zpravy o splneni oddluzeni']);
        $table->addColumn('zspo_id', 'integer', ['comment' => 'Zprava o splneni oddluzeni'])
            ->addColumn('celkova_odmena', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('celkova_odmena_uhrazeno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('hotove_vydaje', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('hotove_vydaje_uhrazeno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vytezek_zpenezeni_rozdeleni', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vytezek_zpenezeni_rozdeleni_uhrazeno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vytezek_zpenezeni_zaji', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vytezek_zpenezeni_zaji_uhrazeno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('zprava_spravce', 'text')
            ->addForeignKey('zspo_id', 'zprava_splneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->addIndex(['zspo_id'], ['unique' => true])
            ->create();
    }
}
