<?php

namespace App\Http\Controllers\Stats;

use App\Http\Controllers\Controller;
use App\Models\InsRizeni;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use App\Models\Statistiky;

class StatsController extends Controller
{
    protected const VOLBA_ROK_VYCHOZI = 2020;
    protected const VOLBA_ROK_MIN = 2008;
    protected const VOLBA_ROK_MAX = 2020;

    protected $obdobi;

    function __construct() {
        $this->obdobi = new \stdClass;
        $this->obdobi->obdobi_nazev = 'Nezvoleno';
        $this->obdobi->nezvoleno = true;
        $this->obdobi->od = Carbon::createFromDate(static::VOLBA_ROK_MIN, 1, 1);
        $this->obdobi->do = Carbon::createFromDate(static::VOLBA_ROK_MAX, 1, 1);
    }

    protected function koncovaDataObdobi(string $obdobi){
        $rozmezi = new \stdClass;

        $rozmezi->obdobi_nazev = $obdobi;

        if(strlen($obdobi) == 4){
            $rok = (int)$obdobi;
            $date = Carbon::createFromDate($rok, 1, 1);
            $rozmezi->od = $date->copy()->startOfYear();
            $rozmezi->do = $date->copy()->endOfYear();
        }else{
            $parts = explode("/", $obdobi);
            $rok = (int)$parts[0];
            $mesic = (int)$parts[1];
            $date = Carbon::createFromDate($rok, $mesic, 1);
            $rozmezi->od = $date->copy()->startOfMonth();
            $rozmezi->do = $date->copy()->endOfMonth();
        }

        return $rozmezi;
    }

    protected function maximalniObdobi(){
        $rozmezi = new \stdClass;
        $rozmezi->obdobi_nazev = 'Nezvoleno';
        $rozmezi->zahrnout_v_nabidce = true;
        $rozmezi->od = Carbon::createFromDate(static::VOLBA_ROK_MIN, 1, 1);
        $rozmezi->do = Carbon::createFromDate(static::VOLBA_ROK_MAX, 1, 1);
        return $rozmezi;
    }

    protected function vyberObdobi($mesice = true){
        $res = [];
        $now = Carbon::createFromDate(static::VOLBA_ROK_MAX, 1, 2);
        $date = Carbon::createFromDate(static::VOLBA_ROK_MIN, 1, 1);

        while($date < $now){
            if($date->month == 1){
                $res[] = $date->year;
            }
            if($mesice)
                $res[] = $date->year . "/" . str_pad($date->month, 2, '0', STR_PAD_LEFT);
            $date->addMonth();
        }

        return $res;
    }

    protected function filtrParamTypOsoby($typOsoby, $filtr){
        if("FN" == $typOsoby){
            $filtr->where('typ_osoby', '=', 'F')
                    ->where('podnikatel', '=', false);
        }else if("FP" == $typOsoby){
            $filtr->where('typ_osoby', '=', 'F')
                    ->where('podnikatel', '=', true);
        }else if("P" == $typOsoby){
            $filtr->where('typ_osoby', '=', 'P');
        }
    }

    protected function filtrParamZpusobReseni($zpusobReseni, $filtr){
        if($zpusobReseni){
            $filtr->where('typ_rizeni', '=', $zpusobReseni);
        }
    }

    protected function filtrParamObdobi($obdobi, $filtr){
        if(!$obdobi) $obdobi = $this->obdobi;

        $filtr
            ->where('datum_zahajeni', '>=', $obdobi->od)
            ->where('datum_zahajeni', '<=', $obdobi->do);

        $this->obdobi = $obdobi;
    }

    protected function getZpusobReseni(Request $request){
        if($request->has("zpusobReseni")){
            $zpusobReseni = $request->get("zpusobReseni");
            if(in_array($zpusobReseni, ["K", "R", "O"]))
                return $zpusobReseni;
        }
        return null;
    }

    protected function getObdobi(Request $request){
        if($request->has("obdobi")){
            $obdobi = $request->get("obdobi");
        }else{
            $obdobi = self::VOLBA_ROK_VYCHOZI;
        }

        return $this->koncovaDataObdobi($obdobi);
    }

    protected function getTypOsoby(Request $request){
        if($request->has("typOsoby")){
            $typOsoby = $request->get("typOsoby");
            if(in_array($typOsoby, ["FN", "FP", "P"]))
                return $typOsoby;
        }
        return null;
    }

    protected function getRok(Request $request, $vychozi = null){
        $rok = null;

        if($request->has("obdobi")){
            if(strlen($request->get("obdobi")) == 4){
                $rok = intval($request->get("obdobi"));
            }
        }

        if(!$rok && $vychozi){
            $rok = $vychozi;
        }

        if($rok){
            $this->obdobi = $this->koncovaDataObdobi($rok);
            return intval($rok);
        }

        return null;
    }

    static function intervalMode($qb, $res = 1, $min = 0, $max = 100, $attrName = 'value'){
        //construct range-keys array
        $widths = \range($min, $max, $res);

        $bins = array();
        foreach($widths as $key => $val) {
            if (!isset($widths[$key + 1])) break;
            $bins[] = $val.'-'. ($widths[$key + 1]);
        }
        //construct flotHistogram count array
        $flotHistogram = \array_fill_keys($bins, 0);

        $i=0;
        foreach($qb as $dataRow) {
            $dataRow->pos = ++$i;
            $time = $dataRow->$attrName;
            $key = $bins[floor(($time-$min)/$res)] ?? null;
            if ($key===null || !isset($flotHistogram[$key])){
                continue; //out of binning range
            }
            ++$flotHistogram[$key];
        }

        return [
            "min" => $min,
            "max" => $max,
            "res" => $res,
            "data" => \array_values($flotHistogram),
        ];
    }

    protected function statView($view, $data){

        $data = $data + [
            'vyberPoMesicich' => false,
        ];
        $data = $data + [
            'nazevHodnoty' => '?',
            'nazevStatistiky' => '?',
            'varianty' => $this->vyberObdobi($data['vyberPoMesicich'] ?? true),
            'obdobi' => $this->obdobi,
            'poznamky' => [],
            'nazevVolbyObdobi' => null,
            'nastaveni' => ['obdobi', 'typOsoby', 'insZpusob'],
            'extraNastaveni' => [],
            'vyraditTypOsoby' => [],
            'povolitPrazdneObdobi' => true,
        ];

        return view($view, $data);
    }
}
