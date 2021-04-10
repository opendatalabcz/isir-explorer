<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DelkaRizeniController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    public static function delkaRizeni(array $conf){

        $conf = $conf + ['zobrazeniTyp' => 'linear'];

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        $maximalniDelka = 365*10;
        $filtr->select('delka_rizeni')
        //$filtr->select(DB::raw('delka_rizeni/365 as delka_rizeni')) // po letech
            ->where('delka_rizeni', '>=', 1)
            ->where('delka_rizeni', '<=', $maximalniDelka)
            ->whereNotNull('delka_rizeni');

        $rows = $filtr->get();

        $histogram = self::intervalMode($rows, 10, 0, $maximalniDelka, 'delka_rizeni');
        //$histogram = self::intervalMode($rows, 1, 0, 10, 'delka_rizeni'); // po letech
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 30;
        $histogram["xtype"] = $conf['zobrazeniTyp'] == "log" ? "log" : "linear";

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Délka řízení (dny)',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public function delkaRizeni_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Délka řízení',
            'jednotkaRozsahu' => 'dní',
            'povolitPrazdneObdobi' => false,
            'extraNastaveni' => ['zobrazeniTyp'],
        ];

        $viewData['delkaRizeni'] = DelkaRizeniController::delkaRizeni([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, static::VOLBA_ROK_VYCHOZI),
            'typOsoby' => $this->getTypOsoby($request),
            'zobrazeniTyp' => $request->get("zobrazeniTyp"),
            'vychoziRozliseni' => 30,
        ]);

        return $this->statView('stats.detail-delkaRizeni', $viewData);
    }

}

