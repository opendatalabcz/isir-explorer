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
          ->addColumn('typ', 'smallinteger', ['null' => false, 'comment' => 'Typ parseru'])
          ->addColumn('verze_dokument', 'string', ['null' => true, 'limit' => 10, 'comment' => 'Oznaceni verze pdf dokumentu (je-li dostupne)'])
          ->addColumn('verze_scraper', 'smallinteger', ['null' => true, 'comment' => 'Verze scraperu (pro dany typ dokumentu), ktery byl pouzit pro precteni'])
          ->addColumn('datum', 'timestamp', ['null' => false, 'comment' => 'Datum precteni dokumentu'])
          ->addIndex(['isir_id'], ['unique' => false])
          ->create();

        /* ====================================================================================== */
        /* ============ Prihlaska pohledavky ============ */

        $table = $this->table('prihlaska_pohledavky', ['id' => false, 'primary_key' => ['id']]);
        $table->addColumn('id', 'integer', ['null' => false])
              ->addColumn('pocet_pohledavek', 'integer')
              ->addColumn('celkova_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('celkova_vyse_nezajistenych', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('celkova_vyse_zajistenych', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('id', 'dokument', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();
            
        $table = $this->table('pp_pohledavka', ['comment' => 'Pohledavka v prihlasce']);
        $table->addColumn('pp_id', 'integer', ['comment' => 'Prihlaska pohledavky'])
              ->addColumn('cislo', 'integer')
              ->addColumn('celkova_vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('vyse_jistiny', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC, 'null' => true])
              ->addColumn('typ', 'smallinteger', ['null' => true])
              ->addColumn('typ_text', 'string', ['null' => true, 'limit' => 50])
              ->addColumn('dalsi_okolnosti', 'text', ['null' => true])
              ->addColumn('duvod_vzniku', 'text', ['null' => true])
              ->addColumn('splatna', 'boolean')
              ->addColumn('podrizena', 'boolean')
              ->addColumn('vykonatelnost', 'boolean')
              ->addForeignKey('pp_id', 'prihlaska_pohledavky', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();
        // TODO detail splatnosti, prislusenstvi, vykonatelnost, podrizenost

        /* ====================================================================================== */
        /* ============ Prehledovy list ============ */

        $table = $this->table('prehledovy_list', ['id' => false, 'primary_key' => ['id'], 'comment' => 'Prehledovy list - souhrn pro nezajistene a zajistene veritele']);
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
              ->addColumn('veritel', 'text')
              ->addColumn('vykonatelne', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('zbyva_uspokojit', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('zjisteno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('pl_id', 'prehledovy_list', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        /* ====================================================================================== */
        /* ============ Zprava pro oddluzeni ============ */

        $table = $this->table('zprava_pro_oddluzeni', ['id' => false, 'primary_key' => ['id']]);
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
            ->create();

        $table = $this->table('zpro_prijem_dluznika', ['comment' => 'Prijem dluznika dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('nazev_platce', 'string', ['null' => true])
            ->addColumn('adresa', 'string', ['null' => true])
            ->addColumn('ico', 'string', ['limit' => 60, 'null' => true])
            ->addColumn('typ', 'string', ['null' => true])
            ->addColumn('vyse', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        $table = $this->table('zpro_distribucni_schema', ['comment' => 'Distribucni schema dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
            ->addColumn('veritel', 'integer', ['comment' => 'Cislo veritele'])
            ->addColumn('castka', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('podil', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        $table = $this->table('zpro_predpoklad_uspokojeni', ['comment' => 'Predpoklad uspokojeni dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
            ->addColumn('uspokojeni', 'smallinteger', ['comment' => 'Typ uspokojeni'])
            ->addColumn('mira', 'decimal', ['comment' => 'Procent', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addColumn('vyse', 'decimal', ['comment' => 'Castka v Kc', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        /* ====================================================================================== */
        /* ============ Zprava o plneni oddluzeni ============ */

        $table = $this->table('zprava_plneni_oddluzeni', ['id' => false, 'primary_key' => ['id']]);
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
              ->create();

        $table = $this->table('zplo_vykaz_prerozdeleni_veritel', ['comment' => 'Vykaz prerozdeleni pro jednotlive veritele']);
        $table->addColumn('zplo_id', 'integer', ['comment' => 'Zprava o plneni oddluzeni'])
              ->addColumn('veritel', 'string')
              ->addColumn('castka', 'decimal', ['comment' => 'Celkova dluzna castka', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addColumn('podil', 'decimal', ['comment' => 'Podil veritele na distr. schematu', 'scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('zplo_id', 'zprava_plneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('zplo_vykaz_prerozdeleni', ['comment' => 'Vykaz prerozdeleni po jednotlivych mesicich pro jednotlive veritele']);
        $table->addColumn('zplo_veritel_id', 'integer', ['comment' => 'Veritel ve vykazu prerozdeleni'])
              ->addColumn('rok', 'smallinteger')
              ->addColumn('mesic', 'smallinteger')
              ->addColumn('mesic_oddluzeni', 'smallinteger')

              ->addColumn('vyplaceno', 'decimal', ['scale' => DEC_SCAL, 'precision' => DEC_PREC])
              ->addForeignKey('zplo_veritel_id', 'zplo_vykaz_prerozdeleni_veritel', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        /* ====================================================================================== */
        /* ============ Zprava o splneni oddluzeni ============ */

        $table = $this->table('zprava_splneni_oddluzeni', ['id' => false, 'primary_key' => ['id']]);
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

        $table = $this->table('zspo_odmena_spravce');
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
            ->create();
    }
}
