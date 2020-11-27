<?php
declare(strict_types=1);

use Phinx\Migration\AbstractMigration;

final class Init extends AbstractMigration
{
    public function change(): void
    {
        /* ====================================================================================== */
        /* ============ Prihlaska pohledavky ============ */

        $table = $this->table('prihlaska_pohledavky');
        $table->addColumn('pocet_pohledavek', 'integer')
              ->addColumn('celkova_vyse', 'float')
              ->addColumn('celkova_vyse_nezajistenych', 'float')
              ->addColumn('celkova_vyse_zajistenych', 'float')
              ->create();
            
        $table = $this->table('pp_pohledavka', ['comment' => 'Pohledavka v prihlasce']);
        $table->addColumn('pp_id', 'integer', ['comment' => 'Prihlaska pohledavky'])
              ->addColumn('cislo', 'integer')
              ->addColumn('celkova_vyse', 'float')
              ->addColumn('vyse_jistiny', 'float')
              ->addColumn('typ', 'smallinteger')
              ->addColumn('dalsi_okolnosti', 'text', ['null' => true])
              ->addColumn('duvod_vzniku', 'text', ['null' => true])
              ->addColumn('splatna', 'boolean')
              ->addColumn('vykonatelnost', 'boolean')
              ->addForeignKey('pp_id', 'prihlaska_pohledavky', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();
        // TODO detail splatnosti, prislusenstvi, vykonatelnost

        /* ====================================================================================== */
        /* ============ Prehledovy list ============ */

        $table = $this->table('prehledovy_list');
        $table->addColumn('celkova_vyse', 'float')
              ->addColumn('vykonatelne', 'float')
              ->addColumn('nevykonatelne', 'float')
              ->addColumn('duplicitni', 'float')
              ->addColumn('neprezkoumavano', 'float')
              ->addColumn('odmitnuto', 'float')
              ->addColumn('podmineno', 'float')
              ->addColumn('popreno', 'float')
              ->addColumn('zbyva_uspokojit', 'float')
              ->addColumn('zjisteno', 'float')
              ->create();

        $table = $this->table('pl_pohledavka', ['comment' => 'Pohledavka v prehledovem listu']);
        $table->addColumn('pl_id', 'integer')
              ->addColumn('celkova_vyse', 'float')
              ->addColumn('cislo_prihlasky', 'smallinteger')
              ->addColumn('cislo_veritele', 'smallinteger')
              ->addColumn('datum_doruceni', 'date')
              ->addColumn('duplicitni', 'float')
              ->addColumn('neprezkoumavano', 'float')
              ->addColumn('nevykonatelne', 'float')
              ->addColumn('odmitnuto', 'float')
              ->addColumn('podmineno', 'float')
              ->addColumn('popreno', 'float')
              ->addColumn('procent', 'float')
              ->addColumn('veritel', 'text')
              ->addColumn('vykonatelne', 'float')
              ->addColumn('zbyva_uspokojit', 'float')
              ->addColumn('zjisteno', 'float')
              ->addForeignKey('pl_id', 'prehledovy_list', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        /* ====================================================================================== */
        /* ============ Zprava pro oddluzeni ============ */

        $table = $this->table('zprava_pro_oddluzeni');
        $table->addColumn('odmena_za_sepsani_navrhu', 'float')
              ->addColumn('povinnen_vydat_obydli', 'string')
              ->addColumn('vyse_zalohy', 'float')
              ->addColumn('vytezek_zpenezeni_obydli', 'float')
              ->addColumn('zpracovatel_navrhu', 'string')
              ->addColumn('prijmy_celkem', 'float')
              ->addColumn('prijmy_komentar', 'text')

              ->addColumn('celkem_majetek_oceneni', 'float')
              ->addColumn('celkem_majetek_nezajisteno', 'float')
              ->addColumn('celkem_majetek_zajisteno', 'float')
              
              ->addColumn('okolnosti_proti_oddluzeni', 'text')
              ->addColumn('navrh_dluznika', 'text')
              ->addColumn('navrh_spravce', 'text')
              
              ->create();

        $table = $this->table('zpro_soupis_majetku', ['comment' => 'Soupis majetku dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ_majetku', 'smallinteger')
            ->addColumn('oceneni', 'float')
            ->addColumn('nezajisteno', 'float')
            ->addColumn('zajisteno', 'float')
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        $table = $this->table('zpro_prijem_dluznika', ['comment' => 'Prijem dluznika dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('nazev_platce', 'string')
            ->addColumn('adresa', 'string')
            ->addColumn('ICO', 'string', ['limit' => 60])
            ->addColumn('typ', 'string')
            ->addColumn('vyse', 'float')
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        $table = $this->table('zpro_distribucni_schema', ['comment' => 'Distribucni schema dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
            ->addColumn('veritel', 'integer', ['comment' => 'Cislo veritele'])
            ->addColumn('castka', 'float')
            ->addColumn('podil', 'float')
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        $table = $this->table('zpro_predpoklad_uspokojeni', ['comment' => 'Predpoklad uspokojeni dle zpravy pro oddluzeni']);
        $table->addColumn('zpro_id', 'integer', ['comment' => 'Zprava pro oddluzeni'])
            ->addColumn('typ', 'boolean', ['comment' => 'Nezajisteny/zajisteny veritel'])
            ->addColumn('uspokojeni', 'smallinteger', ['comment' => 'Typ uspokojeni'])
            ->addColumn('mira', 'float', ['comment' => 'Procent'])
            ->addColumn('vyse', 'float', ['comment' => 'Castka v Kc'])
            ->addForeignKey('zpro_id', 'zprava_pro_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();

        /* ====================================================================================== */
        /* ============ Zprava o plneni oddluzeni ============ */

        $table = $this->table('zprava_plneni_oddluzeni');
        $table->addColumn('doporuceni_spravce', 'text')
              ->addColumn('doporuceni_spravce_oduvodneni', 'text')
              ->addColumn('duvod_neplneni', 'text')
              ->addColumn('plni_povinnosti', 'string')
              ->addColumn('stanovisko_dluznika', 'text')
              ->addColumn('vyjadreni_spravce', 'text')

              ->addColumn('uspokojeni_nez_ocekavana', 'float', ['null' => true, 'comment' => 'Ocekavana mira uspokojeni nezajistenych pohledavek'])
              ->addColumn('uspokojeni_nez_aktualni', 'float' , ['null' => true, 'comment' => 'Aktualni mira uspokojeni nezajistenych pohledavek'])
              ->addColumn('uspokojeni_zaj_ocekavana', 'float', ['null' => true, 'comment' => 'Ocekavana mira uspokojeni zajistenych pohledavek'])
              ->addColumn('uspokojeni_zaj_aktualni', 'float',  ['null' => true, 'comment' => 'Aktualni mira uspokojeni zajistenych pohledavek'])

              ->create();

        $table = $this->table('zplo_vykaz_plneni', ['comment' => 'Vykaz plneni oddluzeni po jednotlivych mesicich']);
        $table->addColumn('zplo_id', 'integer', ['comment' => 'Zprava o plneni oddluzeni'])
              ->addColumn('rok', 'smallinteger')
              ->addColumn('mesic', 'smallinteger')
              ->addColumn('mesic_oddluzeni', 'smallinteger')
              ->addColumn('prijem', 'float')
              ->addColumn('srazky', 'float')
              ->addColumn('zm_nnb', 'float', ['comment' => 'Zivotni minimum + Normovane naklady na bydleni'])

              ->addColumn('vyzivovane_osoby', 'smallinteger')
              ->addColumn('nepostizitelne', 'float')
              ->addColumn('postizitelne', 'float')
              ->addColumn('vraceno_dluznikum', 'float')
              ->addColumn('mimoradny_prijem', 'float')
              ->addColumn('darovaci_smlouva', 'float')
              ->addColumn('k_prerozdeleni', 'float')
              ->addColumn('odmena_IS', 'float')
              ->addColumn('vyzivne', 'float')
              ->addColumn('ostatnim_veritelum', 'float')

              ->addColumn('celkem_prerozdeleno', 'float', ['comment' => 'Kc doposud rozdeleno veritelum k tomuto mesici'])
              ->addColumn('mira_uspokojeni', 'float', ['comment' => 'Aktualni mira uspokojeni k tomuto mesici'])
              ->addColumn('mira_uspkojeni_ocekavana', 'float', ['comment' => 'Ocekavana mira uspokojeni k tomuto mesici'])

              ->addForeignKey('zplo_id', 'zprava_plneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('zplo_vykaz_prerozdeleni_veritel', ['comment' => 'Vykaz prerozdeleni pro jednotlive veritele']);
        $table->addColumn('zplo_id', 'integer', ['comment' => 'Zprava o plneni oddluzeni'])
              ->addColumn('veritel', 'string')
              ->addColumn('castka', 'float', ['comment' => 'Celkova dluzna castka'])
              ->addColumn('podil', 'float', ['comment' => 'Podil veritele na distr. schematu'])
              ->addForeignKey('zplo_id', 'zprava_plneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        $table = $this->table('zplo_vykaz_prerozdeleni', ['comment' => 'Vykaz prerozdeleni po jednotlivych mesicich pro jednotlive veritele']);
        $table->addColumn('zplo_veritel_id', 'integer', ['comment' => 'Veritel ve vykazu prerozdeleni'])
              ->addColumn('rok', 'smallinteger')
              ->addColumn('mesic', 'smallinteger')
              ->addColumn('mesic_oddluzeni', 'smallinteger')

              ->addColumn('vyplaceno', 'float')
              ->addForeignKey('zplo_veritel_id', 'zplo_vykaz_prerozdeleni_veritel', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
              ->create();

        /* ====================================================================================== */
        /* ============ Zprava o splneni oddluzeni ============ */

        $table = $this->table('zprava_splneni_oddluzeni');
        $table->addColumn('oddluzeni_povoleno', 'date', ['null' => true])
              ->addColumn('oddluzeni_schvaleno', 'date', ['null' => true])
              ->addColumn('zahajeno', 'date', ['null' => true])
              ->addColumn('zjisteni_upadku', 'date', ['null' => true])
              ->addColumn('posledni_splatka', 'date', ['null' => true])
              ->addColumn('zaslani_vyzvy_ukonceni_srazek', 'date', ['null' => true])

              ->addColumn('doporuceni_spravce', 'text')
              ->addColumn('doporuceni_spravce_oduvodneni', 'text')
              ->addColumn('zprava_o_prubehu', 'text')

              ->addColumn('predpoklad_uspokojeni_nezaj_mira', 'float')
              ->addColumn('predpoklad_uspokojeni_nezaj_vyse', 'float')
              ->addColumn('uspokojeni_nezaj_mira', 'float')
              ->addColumn('uspokojeni_nezaj_vyse', 'float')
              ->addColumn('uspokojeni_zaj_mira', 'float')
              ->addColumn('uspokojeni_zaj_vyse', 'float')
              ->addColumn('preplatek', 'float')

              ->create();

        $table = $this->table('zspo_odmena_spravce');
        $table->addColumn('zspo_id', 'integer', ['comment' => 'Zprava o splneni oddluzeni'])
            ->addColumn('celkova_odmena', 'float')
            ->addColumn('celkova_odmena_uhrazeno', 'float')
            ->addColumn('hotove_vydaje', 'float')
            ->addColumn('hotove_vydaje_uhrazeno', 'float')
            ->addColumn('vytezek_zpenezeni_rozdeleni', 'float')
            ->addColumn('vytezek_zpenezeni_rozdeleni_uhrazeno', 'float')
            ->addColumn('vytezek_zpenezeni_zaji', 'float')
            ->addColumn('vytezek_zpenezeni_zaji_uhrazeno', 'float')
            ->addColumn('zprava_spravce', 'text')
            ->addForeignKey('zspo_id', 'zprava_splneni_oddluzeni', 'id', ['delete'=> 'CASCADE', 'update'=> 'CASCADE'])
            ->create();
    }
}