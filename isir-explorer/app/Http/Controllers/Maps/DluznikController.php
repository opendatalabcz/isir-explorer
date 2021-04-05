<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Controller;
use App\Models\InsRizeni;
use App\Models\Statistiky;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DluznikController extends MapController
{
    const FIXED_DECIMAL = 4;

    protected $celkemPocetIns = 0;

    protected function dataKrajeVekDluznika(Request $request){
        $filtr = InsRizeni::query();

        $obdobi = $this->getObdobi($request);
        $typOsoby = $this->getTypOsoby($request);
        $zpusobReseni = $this->getZpusobReseni($request);

        $this->filtrParamObdobi($obdobi, $filtr);
        $this->filtrParamTypOsoby($typOsoby, $filtr);
        $this->filtrParamZpusobReseni($zpusobReseni, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->where('vek_dluznika','>=',18)
            ->select('kraj', DB::raw('count(*) as pocet'), DB::raw('sum(vek_dluznika) as vek_dluznika'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = round($row->vek_dluznika / $row->pocet, self::FIXED_DECIMAL);
            $this->celkemPocetIns += $row->pocet;
        }
        return $kraje;
    }

    public function vek(Request $request){
        $kraje = $this->dataKrajeVekDluznika($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Průměrný věk',
            'nazevHodnotyInfobox' => 'Věk',
            'nazevMapy' => 'Průměrný věk dlužníka',
            'poznamky' => [
                'V kalkulaci je použit věk dlužníka v době zahájení řízení. '
                .'Celkový počet insolvencí zahrnutých v kalkulaci pro toto období: ' . $this->celkemPocetIns . '.'
            ],
            'jeCastka' => true,
            'inverze' => true,
            'vyberPoMesicich' => false,
            'vyraditTypOsoby' => ['P'],
        ]);
    }
}
