<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;

class OddlMiraUspokojeniController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    public const ZOBRAZ_MIRA_SKUTECNA = 0;
    public const ZOBRAZ_MIRA_PREDPOKLAD = 1;
    public const ZOBRAZ_MIRA_ROZDIL = 2;

    public static function miraUspokojeni(array $conf){

        $conf = $conf + ['zobrazeniTyp' => 'linear'];

        $filtr = InsRizeni::query();

        self::filtrObdobiUkonceni($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        $filtr->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
              ->join('zprava_splneni_oddluzeni', 'zprava_splneni_oddluzeni.id', '=', 'stat_oddluzeni.zspo_id');
              //->join('zprava_pro_oddluzeni', 'zprava_pro_oddluzeni.id', '=', 'stat_oddluzeni.zpro_id');

        if(self::ZOBRAZ_MIRA_ROZDIL == $conf['miraUspokojeni']){
            $filtr->select('n_uspokojeni_vs_predpoklad')
            ->where('n_uspokojeni_vs_predpoklad', '>=', -100)
            ->where('n_uspokojeni_vs_predpoklad', '<=', 100);
            $rows = $filtr->get();
            $histogram = self::intervalMode($rows, 1, -100, 100, 'n_uspokojeni_vs_predpoklad');
        } else if(self::ZOBRAZ_MIRA_PREDPOKLAD == $conf['miraUspokojeni']){
            $filtr->select('n_predpoklad_uspokojeni_mira')
            ->where('n_predpoklad_uspokojeni_mira', '>', 0)
            ->where('n_predpoklad_uspokojeni_mira', '<=', 100);
            $rows = $filtr->get();
            $histogram = self::intervalMode($rows, 1, 0, 100, 'n_predpoklad_uspokojeni_mira');
        } else {
            $filtr->select('stat_oddluzeni.n_uspokojeni_mira as so_n_uspokojeni_mira')
            ->where('stat_oddluzeni.n_uspokojeni_mira', '>', 0)
            ->where('stat_oddluzeni.n_uspokojeni_mira', '<=', 100);
            $rows = $filtr->get();
            $histogram = self::intervalMode($rows, 1, 0, 100, 'so_n_uspokojeni_mira');
        }

        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 1;
        $histogram["ytype"] = $conf['zobrazeniTyp'] == "log" ? "log" : "linear";

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Procentuální míra uspokojení věřitelů',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public function miraUspokojeni_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Oddlužení – míra uspokojení věřitelů',
            'jednotkaRozsahu' => ' %',
            'povolitPrazdneObdobi' => true,
            'nazevVolbyObdobi' => 'Období ukončení řízení',
            'nastaveni' => ['obdobi', 'typOsoby'],
            'extraNastaveni' => ['zobrazeniTyp', 'miraUspokojeni'],
            'vyraditTypOsoby' => ['P'],
            'poznamky' => [
                'Zobrazovaná míra uspokojení se týká pouze nezajištěných věřitelů.',
                'Zahrnuta jsou data pouze pro řízení, pro která se podařilo přečíst data o míře uspokojení ze Zprávy o splnění oddlužení.'
            ],
        ];

        $viewData['miraUspokojeni'] = self::miraUspokojeni([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, null),
            'typOsoby' => $this->getTypOsoby($request),
            'vychoziRozliseni' => 1,
            'zobrazeniTyp' => $request->get("zobrazeniTyp"),
            'miraUspokojeni' => $request->get("miraUspokojeni"),
        ]);

        return $this->statView('stats.detail-miraUspokojeni', $viewData);
    }

}

