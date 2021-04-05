<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Controller;
use App\Models\InsRizeni;
use App\Models\Statistiky;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class PohledavkyController extends MapController
{
    const FIXED_DECIMAL = 4;

    protected $celkemPocetIns = 0;

    protected function dataKraje(Request $request){
        $filtr = InsRizeni::query();

        $obdobi = $this->getObdobi($request);
        $typOsoby = $this->getTypOsoby($request);
        $zpusobReseni = $this->getZpusobReseni($request);

        $this->filtrParamObdobi($obdobi, $filtr);
        $this->filtrParamTypOsoby($typOsoby, $filtr);
        $this->filtrParamZpusobReseni($zpusobReseni, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->join('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->select('kraj', DB::raw('count(*) as pocet'), DB::raw('sum(celkova_vyse) as celkova_vyse'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = $row->celkova_vyse;
            $this->celkemPocetIns += $row->pocet;
        }
        return $kraje;
    }

    public function pohledavky(Request $request){
        $kraje = $this->dataKraje($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Celková hodnota<br>pohledávek (Kč)',
            'nazevHodnotyInfobox' => 'Výše (Kč)',
            'nazevMapy' => 'Výše přihlášených pohledávek',
            'poznamky' => [
                'Započteny jsou pouze pohledávky, z kterých bylo možné údaje automaticky přečíst. Absolutní hodnoty částek proto nereflektují skutečný stav - nástroj slouží pouze pro orientační srovnání mezi kraji ČR.'
                .'Celkový počet insolvencí zahrnutých v kalkulaci pro toto období: ' . $this->celkemPocetIns . '.'
            ],
            'jeCastka' => true,
        ]);
    }
}
