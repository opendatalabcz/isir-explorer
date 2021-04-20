<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;

class OddlMajetekController extends StatsController
{
    use StatsFilters;

    const VYCHOZI_ROZSAH = 3;

    public const TYP_MAJETKU = [
        0 => ['nazev' => 'Celkový majetek dlužníka'],
        1 => ['nazev' => 'Finanční prostředky'],
        2 => ['nazev' => 'Movitý'],
        3 => ['nazev' => 'Nemovitý'],
        4 => ['nazev' => 'Ostatní'],
        4 => ['nazev' => 'Pohledávky'],
    ];

    public static function majetekDluznika(array $conf){

        $conf = $conf + ['zobrazeniTyp' => 'linear', 'typMajetku' => 0];

        $filtr = InsRizeni::query();

        if(!empty($conf['idRozsahu'])){
            self::aplikovatDefiniciRozsahu($conf, $conf['idRozsahu']);
        }

        if(empty($conf['max']) || empty($conf['res'])){
            self::aplikovatDefiniciRozsahu($conf, self::VYCHOZI_ROZSAH);
        }

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        $filtr->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
              ->join('zprava_pro_oddluzeni', 'zprava_pro_oddluzeni.id', '=', 'stat_oddluzeni.zpro_id');

        if( 0 == $conf['typMajetku'] ){
            $filtr->select('celkem_majetek_oceneni AS majetek')
                ->where('celkem_majetek_oceneni', '>=', 0);
        }else{
            if(empty(self::TYP_MAJETKU[$conf['typMajetku']]))
                abort(404);
            $filtr->select('oceneni AS majetek')
                ->join('zpro_soupis_majetku', 'zpro_soupis_majetku.zpro_id', '=', 'stat_oddluzeni.zpro_id')
                ->where('typ_majetku', '=', $conf['typMajetku'])
                ->where('oceneni', '>=', 0);
        }

        $rows = $filtr->get();

        $histogram = self::intervalMode($rows, $conf['res'], 0, $conf['max'], 'majetek');
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? $conf['res'];
        self::aplikovatNastaveniOs($histogram, $conf, "Y");

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Majetek dlužníka (ocenění v Kč)',
                'y' => 'Počet dlužníků',
            ],
        ];
    }

    public function majetekDluznika_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Oddlužení – majetek dlužníka',
            'jednotkaRozsahu' => 'Kč',
            'povolitPrazdneObdobi' => true,
            'nastaveni' => ['obdobi', 'typOsoby'],
            'extraNastaveni' => ['zobrazeniTyp', 'idRozsahu', 'typMajetku'],
            'rozsahyZobrazeni' => self::ROZSAH_ZOBRAZENI,
            'vyraditTypOsoby' => ['P'],
            'vychoziZobrazeniTyp' => 'logxy',
            'vychoziLogOsa' => 'Y',
            'poznamky' => [
                'Zahrnuta jsou data pouze z insolvenčních řízení, pro která se podařilo přečíst data o majetku dlužníka ze Zprávy pro oddlužení.'
            ],
        ];

        $viewData['majetekDluznika'] = self::majetekDluznika([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, null),
            'typOsoby' => $this->getTypOsoby($request),
            'zobrazeniTyp' => $request->get("zobrazeniTyp", "log"),
            'idRozsahu' => $request->get("idRozsahu"),
            'typMajetku' => intval($request->get("typMajetku", 0)),
        ]);

        return $this->statView('stats.detail-majetekDluznika', $viewData);
    }

}

