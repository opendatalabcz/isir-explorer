<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class OddlFormaController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    public const FORMA_ODDLUZENI_DL = [
        "1. plněním splátkového kalendáře" => "Splátkový kalendář",
        "2. zpeněžením majetkové podstaty" => "Zpeněžení majetku",
        "3. plněním splátkového kalendáře se zpeněžením majetkové podstaty" => "Splátkový kalendář + Zpeněžení majetku",
    ];

    public const FORMA_ODDLUZENI_IS = [
        "1. plnění splátkového kalendáře" => "Splátkový kalendář",
        "2. zpeněžení majetkové podstaty" => "Zpeněžení majetku",
        "3. plnění splátkového kalendáře se zpeněžením majetkové podstaty" => "Splátkový kalendář + Zpeněžení majetku",
    ];

    protected static function nazevFormyOddluzeni($row, $conf){
        if('DL' == $conf['navrhujiciStrana'] && isset(self::FORMA_ODDLUZENI_IS[$row['forma']]))
            return self::FORMA_ODDLUZENI_IS[$row['forma']];
        if('IS' == $conf['navrhujiciStrana'] && isset(self::FORMA_ODDLUZENI_DL[$row['forma']]))
            return self::FORMA_ODDLUZENI_DL[$row['forma']];
        return null;
    }

    public static function formaOddluzeni(array $conf){

        $conf = $conf + ['navrhujiciStrana' => 'IS'];

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);

        $filtr->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
              ->join('zprava_pro_oddluzeni', 'zprava_pro_oddluzeni.id', '=', 'stat_oddluzeni.zpro_id')
              ->orderBy('pocet', 'DESC');

        if('DL' == $conf['navrhujiciStrana']){
            $filtr->select('navrh_dluznika AS forma', DB::raw('count(*) AS pocet'))
                  ->groupBy('navrh_dluznika');
        }else{
            $filtr->select('navrh_spravce AS forma', DB::raw('count(*) AS pocet'))
                  ->groupBy('navrh_spravce');
        }

        $rows = $filtr->get();

        $res = [];
        foreach ($rows as $row) {
            $nazev = self::nazevFormyOddluzeni($row, $conf);
            if(!$nazev) continue;
            $res[$nazev] = $row->pocet;
            self::$celkemPocetIns += $row->pocet;
        }

        return [
            'data' => $res,
            'labels' => [
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public function formaOddluzeni_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Navrhovaná forma oddlužení',
            'nastaveni' => ['obdobi'],
            'extraNastaveni' => ['navrhujiciStrana'],
            'poznamky' => [
                'Zahrnuta jsou data pouze z insolvenčních řízení, pro která se podařilo přečíst navrhované formy oddlužení ze Zprávy pro oddlužení.'
            ],
        ];

        $viewData['formaOddluzeni'] = self::formaOddluzeni([
            'rok' => $this->getRok($request),
            'navrhujiciStrana' => $request->get("navrhujiciStrana"),
        ]);

        return $this->statView('stats.detail-formaOddluzeni', $viewData);
    }
}

