<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class PocetInsController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    public static function pocetNovychInsPoMesicich(array $conf){
        $conf = $conf + [
            'poLetech' => 0,
        ];

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        if($conf['poLetech'] == 1){
            $filtr->select('zahajeni_r', DB::raw('count(*) as pocet'))
                ->where('zahajeni_r', '<=', static::VOLBA_ROK_MAX)
                ->groupBy('zahajeni_r')
                ->orderBy('zahajeni_r', 'ASC');
        }else{
            $filtr->select('zahajeni_r', 'zahajeni_m', DB::raw('count(*) as pocet'))
                ->groupBy('zahajeni_r', 'zahajeni_m')
                ->orderBy('zahajeni_r', 'ASC')
                ->orderBy('zahajeni_m', 'ASC');
        }

        $rows = $filtr->get();

        $mesice = [];
        foreach ($rows as $row) {
            $mesic = ($conf['poLetech'] == 1) ? $row->zahajeni_r : ($row->zahajeni_r . "/" . $row->zahajeni_m);
            $mesice[$mesic] = $row->pocet;
            self::$celkemPocetIns += $row->pocet;
        }
        return [
            'data' => $mesice,
            'labels' => [
                'x' => 'Měsíc',
                'y' => 'Počet nových insolvencí',
            ],
        ];
    }

    public function pocet_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Počet insolvencí',
            'extraNastaveni' => ['poLetech'],
        ];

        $poLetech = $request->get('poLetech') == 1 ? 1 : 0;
        $viewData['pocetNovych'] = PocetInsController::pocetNovychInsPoMesicich([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $poLetech ? null : $this->getRok($request),
            'typOsoby' => $this->getTypOsoby($request),
            'poLetech' => $poLetech,
        ]);

        return $this->statView('stats.detail-pocet', $viewData);
    }

}

