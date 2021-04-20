<?php

namespace App\Http\Controllers\Maps;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class OddluzeniController extends MapController
{
    const FIXED_DECIMAL = 4;
    const PRIJMY_MAXIMUM_PRO_PRUMER = 60000;
    protected const VOLBA_ROK_MIN = 2012;

    protected $celkemPocetIns = 0;

    protected function dataKrajeUspesnost(Request $request){
        $filtr = InsRizeni::query();

        $obdobi = $this->getObdobi($request);
        $typOsoby = $this->getTypOsoby($request);

        $this->filtrParamObdobi($obdobi, $filtr);
        $this->filtrParamTypOsoby($typOsoby, $filtr);

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

    protected function dataKrajeZrusena(Request $request){
        $filtr = InsRizeni::query();

        $obdobi = $this->getObdobi($request);
        $typOsoby = $this->getTypOsoby($request);

        $this->filtrParamObdobi($obdobi, $filtr);
        $this->filtrParamTypOsoby($typOsoby, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->where('vysledek_oddluzeni','=',false)
            ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->select('kraj', DB::raw('count(*) as pocet'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = $row->pocet;
            $this->celkemPocetIns += $row->pocet;
        }
        return $kraje;
    }

    protected function dataKrajeOsvobozeni(Request $request){
        $filtr = InsRizeni::query();

        $obdobi = $this->getObdobi($request);
        $typOsoby = $this->getTypOsoby($request);

        $this->filtrParamObdobi($obdobi, $filtr);
        $this->filtrParamTypOsoby($typOsoby, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->where('vysledek_oddluzeni','=',true)
            ->where('n_osvobozeno','>',0)
            ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->select('kraj', DB::raw('count(*) as pocet'), DB::raw('sum(n_osvobozeno) as celkem_osvobozeni'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = round($row->celkem_osvobozeni / $row->pocet, 4);
            $this->celkemPocetIns += $row->pocet;
        }
        return $kraje;
    }

    protected function dataKrajePrijmyDluznika(Request $request){
        $filtr = InsRizeni::query();

        $obdobi = $this->getObdobi($request);
        $typOsoby = $this->getTypOsoby($request);

        $this->filtrParamObdobi($obdobi, $filtr);
        $this->filtrParamTypOsoby($typOsoby, $filtr);

        $rows = $filtr
            ->whereNotNull('kraj')
            ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->join('zprava_pro_oddluzeni', 'zprava_pro_oddluzeni.id', '=', 'stat_oddluzeni.zpro_id')
            ->whereNotNull('prijmy_celkem')
            ->where('prijmy_celkem', '>=', 0)
            ->where('prijmy_celkem', '<=', self::PRIJMY_MAXIMUM_PRO_PRUMER)
            ->select('kraj', DB::raw('count(*) as pocet'), DB::raw('sum(prijmy_celkem) as prijmy_celkem'))
            ->groupBy('kraj')
            ->get();

        $kraje = [];
        foreach ($rows as $row) {
            $kraje[$row->kraj] = round($row->prijmy_celkem / $row->pocet, 4);
            $this->celkemPocetIns += $row->pocet;
        }
        return $kraje;
    }

    protected function filtrParamObdobi($obdobi, $filtr){
        $filtr
            ->where('ukonceni_oddluzeni', '>=', $obdobi->od)
            ->where('ukonceni_oddluzeni', '<=', $obdobi->do);

        $this->obdobi = $obdobi;
    }

    public function uspesnost(Request $request){
        $kraje = $this->dataKrajeUspesnost($request);

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
            'nazevVolbyObdobi' => 'Období ukončení řízení',
            'vyraditTypOsoby' => ['P'],
            'nastaveni' => ['obdobi', 'typOsoby'],
        ]);
    }

    public function zrusena(Request $request){
        $kraje = $this->dataKrajeZrusena($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Zrušená oddlužení',
            'nazevHodnotyInfobox' => 'Zrušená oddlužení',
            'nazevMapy' => 'Zrušená oddlužení',
            'poznamky' => [
                'Oddlužení je zrušeno v případech např. když dlužník neplní zákonnem stanovené podmínky oddlužení nebo neusiluje o uspokojení pohledávek věřitelů v maximální míře. '
                .'Jako zrušená se v této statistice považují taková oddlužení, kde insolvenční správce doporučí zrušení oddlužení ve Zprávě o splnění oddlužení. '
                .'Celkový počet insolvencí zahrnutých v kalkulaci pro toto období: ' . $this->celkemPocetIns . '.'
            ],
            'vyberPoMesicich' => false,
            'nazevVolbyObdobi' => 'Období ukončení řízení',
            'vyraditTypOsoby' => ['P'],
            'nastaveni' => ['obdobi', 'typOsoby'],
        ]);
    }

    public function osvobozeni(Request $request){
        $kraje = $this->dataKrajeOsvobozeni($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Průměrná výše<br>osvobození (Kč)',
            'nazevHodnotyInfobox' => 'Výše (Kč)',
            'nazevMapy' => 'Oddlužení – výše osvobození od dluhů',
            'poznamky' => [
                'V případě úspěšného splnění oddlužení je dlužník osvobozen od dosud neuhrazených částí dluhů. Ve statistice je zobrazena průměrná výše tohoto osvobození a to pouze pro případy, kdy dlužník po skončení oddlužení neuhradil 100% svých dluhů. '
                .'Jsou zahrnuta osvobození vyplývající pouze z pohledávek nezajištěných věřitelů. '
                .'Celkový počet insolvencí zahrnutých v kalkulaci pro toto období: ' . $this->celkemPocetIns . '.'
            ],
            'jeCastka' => true,
            'vyberPoMesicich' => false,
            'nazevVolbyObdobi' => 'Období ukončení řízení',
            'vyraditTypOsoby' => ['P'],
            'nastaveni' => ['obdobi', 'typOsoby'],
        ]);
    }

    public function prijmyDluznika(Request $request){
        $kraje = $this->dataKrajePrijmyDluznika($request);

        return $this->mapView([
            'data' => $kraje,
            'nazevHodnoty' => 'Průměrné příjmy (Kč)',
            'nazevHodnotyInfobox' => 'Výše (Kč)',
            'nazevMapy' => 'Oddlužení – průměrné příjmy dlužníka',
            'poznamky' => [
                'Celkový počet insolvencí zahrnutých v kalkulaci pro toto období: ' . $this->celkemPocetIns . '.'
            ],
            'jeCastka' => true,
            'vyberPoMesicich' => false,
            'inverze' => true,
            'nazevVolbyObdobi' => 'Období ukončení řízení',
            'vyraditTypOsoby' => ['P'],
            'nastaveni' => ['obdobi', 'typOsoby'],
        ]);
    }
}
