<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Controller;
use App\Models\InsRizeni;
use App\Models\Statistiky;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class OddluzeniController extends MapController
{
    const FIXED_DECIMAL = 4;

    protected $celkemPocetIns = 0;

    protected function dataKraje(Request $request){
        $filtr = InsRizeni::query();

        $this->filtrParamObdobi($request, $filtr);

        $this->filtrParamTypOsoby($request, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->where('vysledek_oddluzeni','=',true)
            ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->select('kraj', DB::raw('count(*) as pocet'), DB::raw('sum(n_uspokojeni_mira) as celkem_uspokojeni_mira'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = round($row->celkem_uspokojeni_mira / $row->pocet, 4);
            $this->celkemPocetIns += $row->pocet;
        }
        return $kraje;
    }

    protected function filtrParamObdobi(Request $request, $filtr){
        if($request->has("obdobi")){
            $obdobi = $request->get("obdobi");
            $obdobi = $this->koncovaDataObdobi($obdobi);
        }else{
            $obdobi = $this->maximalniObdobi();
        }

        $filtr
            ->where('datum_zahajeni', '>=', $obdobi->od)
            ->where('datum_zahajeni', '<=', $obdobi->do);

        $this->obdobi = $obdobi;
    }

    public function uspesnost(Request $request){
        $kraje = $this->dataKraje($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Míra uspokojení (%)',
            'nazevHodnotyInfobox' => 'Míra uspokojení (%)',
            'nazevMapy' => 'Úspěšnost oddlužení',
            'poznamky' => [
                'Za úspěšnost oddlužení se zde považuje míra uspokojení pohledávek nezajištěných věřitelů po skončení oddlužení (pouze oddlužení, která nejsou zrušena). V mapě je zobrazena průměrná úspěšnost pro jednotlivé kraje. '
                .'Celkový počet insolvencí zahrnutých v kalkulaci pro toto období: ' . $this->celkemPocetIns . '.'
            ],
            'jeCastka' => true,
            'inverze' => true,
            'vyberPoMesicich' => false,
            'nastaveni' => ['obdobi', 'typOsoby'],
        ]);
    }
}
