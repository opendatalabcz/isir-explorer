<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Controller;
use App\Models\InsRizeni;
use App\Models\Statistiky;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class PocetInsolvenciController extends MapController
{
    const FIXED_DECIMAL = 4;

    protected function dataKraje(Request $request){
        $filtr = InsRizeni::query();

        $this->filtrParamObdobi($request, $filtr);

        $this->filtrParamTypOsoby($request, $filtr);

        $this->filtrParamZpusobReseni($request, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->select('kraj', DB::raw('count(*) as pocet'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = $row->pocet;
        }
        return $kraje;
    }

    public function insolvence(Request $request){
        $kraje = $this->dataKraje($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Insolvencí',
            'nazevMapy' => 'Počet insolvencí',
        ]);
    }


    public function insolvenceNaObyvatele(Request $request){

        $kraje = $this->dataKraje($request);

        $datarow = Statistiky::where('nazev','=','data.csu.kraje.obyvatele')
            ->where('rok','=',2020)
            ->first();
        $obyvateleKraju = json_decode($datarow->data, true);

        $celkem = 0;
        foreach ($kraje as $key => $val) {
            $celkem += $val;
            $kraje[$key] = number_format(
                round(($kraje[$key] / $obyvateleKraju[$key]) * 100, self::FIXED_DECIMAL)
            , self::FIXED_DECIMAL);
        }

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Míra populace<br>v insolvenci (%)',
            'nazevHodnotyInfobox' => 'Populace v insolvenci (%)',
            'nazevMapy' => 'Míra insolvencí dle populace krajů',
            'poznamky' => [
                'Hodnota procentuální míry populace v insolvenci je počítána jako podíl počtu insolvencí zahájených '
                .'v daném období odpovídajícím zadaným kritériím a počtu obyvatel krajů dle ČSÚ k&nbsp;datu 1. 1. 2020. '
                .'Celkový počet insolvencí odpovídající paremetrům v tomto období: ' . $celkem . '.'
            ],
        ]);
    }
}
