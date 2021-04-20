<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class OsobaController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    public static function typOsoby(array $conf){

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);

        $filtr->select('typ_osoby', 'podnikatel', DB::raw('count(*) as pocet'))
            ->whereNotNull('typ_osoby')
            ->groupBy('typ_osoby', 'podnikatel')
            ->orderBy('typ_osoby', 'ASC');

        $rows = $filtr->get();


        $res = [];
        foreach ($rows as $row) {
            $nazev = self::nazevTypuOsoby($row);
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



    public static function vekDluznika(array $conf){

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);

        $filtr->select('vek_dluznika')
            ->whereNotNull('vek_dluznika')
            ->where('typ_osoby', '=', 'F');

        $rows = $filtr->get();


        $histogram = self::intervalMode($rows, 1, 0, 100, 'vek_dluznika');
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 10;

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Věk',
                'y' => 'Počet dlužníků',
            ],
        ];
    }

    public function vek_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Věk dlužníka',
            'jednotkaRozsahu' => 'let',
            'povolitPrazdneObdobi' => true,
        ];

        $viewData['vekDluznika'] = OsobaController::vekDluznika([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request),
            'typOsoby' => $this->getTypOsoby($request),
            'vychoziRozliseni' => 1,
        ]);

        return $this->statView('stats.detail-vek', $viewData);
    }

    public function typOsoby_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Typ osoby dlužníka',
            'nastaveni' => ['obdobi', 'insZpusob'],
        ];

        $viewData['typOsoby'] = OsobaController::typOsoby([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request),
        ]);

        return $this->statView('stats.detail-typOsoby', $viewData);
    }
}

