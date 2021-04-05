<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class PohledavkyController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    public static function pohledavky(array $conf){

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        $filtr->select('stat_pohledavky.pohledavky_pocet')
            ->join('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->where('pohledavky_pocet', '>=', 1)
            ->where('pohledavky_pocet', '<=', 200)
            ->whereNotNull('delka_rizeni');

        $rows = $filtr->get();

        $histogram = self::intervalMode($rows, 1, 0, 200, 'pohledavky_pocet');
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 5;

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Počet přihlášených pohledávek',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public function pohledavky_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Počet pohledávek',
            'jednotkaRozsahu' => 'pohledávek',
            'povolitPrazdneObdobi' => false,
        ];

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, static::VOLBA_ROK_VYCHOZI),
            'typOsoby' => $this->getTypOsoby($request),
            'vychoziRozliseni' => 5,
        ]);

        return $this->statView('stats.detail-pohledavky', $viewData);
    }

}

