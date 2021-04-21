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
        $maximalniDelkaMesice = ceil($maximalniDelka/30);
        //$filtr->select('delka_rizeni')
        $filtr->select(DB::raw('delka_rizeni/30 as delka_rizeni_m')) // po letech
            ->where('delka_rizeni', '>=', 1)
            ->where('delka_rizeni', '<=', $maximalniDelka)
            ->whereNotNull('delka_rizeni');

        $rows = $filtr->get();

        $histogram = self::intervalMode($rows, 1, 0, $maximalniDelkaMesice, 'delka_rizeni_m');
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 1;
        self::aplikovatNastaveniOs($histogram, $conf);

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Délka řízení (měsíce)',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public function delkaRizeni_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Délka řízení',
            'jednotkaRozsahu' => 'měsíců',
            'povolitPrazdneObdobi' => true,
            'extraNastaveni' => ['zobrazeniTyp'],
            'poznamky' => [
                'Zahrnuty jsou pouze délky již ukončených řízení.'
            ],
        ];

        $viewData['delkaRizeni'] = DelkaRizeniController::delkaRizeni([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request),
            'typOsoby' => $this->getTypOsoby($request),
            'zobrazeniTyp' => $request->get("zobrazeniTyp"),
            'vychoziRozliseni' => 1,
        ]);

        return $this->statView('stats.detail-delkaRizeni', $viewData);
    }

}

