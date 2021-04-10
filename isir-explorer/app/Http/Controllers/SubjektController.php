<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use App\Models\Veritel;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class SubjektController extends Controller
{

    const TYP_VERITEL = "V";
    const TYP_SPRAVCE = "S";

    protected function typyRizeniSubjektuZaRok($idSubjektu, $rok, $typSubjektu){
        $date = Carbon::createFromDate($rok, 1, 1);
        $od = $date->copy()->startOfYear();
        $do = $date->copy()->endOfYear();

        if(self::TYP_SPRAVCE == $typSubjektu){
            $typyRizeni = DB::table('stat_spravce_ins')
                    ->where('stat_spravce_ins.id_spravce', '=', $idSubjektu)
                    ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins');
        }else{
            $typyRizeni = DB::table('stat_veritel_ins')
                    ->where('stat_veritel_ins.id_veritel', '=', $idSubjektu)
                    ->join('stat_vec', 'stat_vec.id', '=', 'stat_veritel_ins.id_ins');
        }

        $typyRizeni = $typyRizeni
                ->join('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->select(
                    'typ_rizeni',
                    DB::raw('count(*) as pocet'),
                    DB::raw('sum(celkova_vyse) as celkova_vyse'),
                    DB::raw('sum(pohledavky_pocet) as pohledavky_pocet'),
                    DB::raw('sum(popreno) as pohledavky_popreno')
                )
                ->groupBy('typ_rizeni')
                ->where('datum_zahajeni', '>=', $od)
                ->where('datum_zahajeni', '<=', $do)
                ->get();

        return $typyRizeni;
    }

    protected function typyRizeniSubjektu($idSubjektu, $typSubjektu){
        $rok = intval(date("Y"));
        $roky = [$rok-3, $rok-2, $rok-1];
        $result = [];
        foreach ($roky as $rok) {
            $rows = $this->typyRizeniSubjektuZaRok($idSubjektu, $rok, $typSubjektu);
            $dataZaRok = [];
            $celkemZaRok = 0;
            foreach ($rows as $row) {
                $dataZaRok[$row->typ_rizeni] = $row->pocet;
                $dataZaRok[$row->typ_rizeni . "_vyse"] = intval($row->celkova_vyse);
                $dataZaRok[$row->typ_rizeni . "_pohl"] = $row->pohledavky_pocet;
                $dataZaRok[$row->typ_rizeni . "_popreno"] = floatval($row->pohledavky_popreno);
                $celkemZaRok += $row->pocet;
            }
            if($celkemZaRok)
                $result[$rok] = $dataZaRok;
        }
        return $result;
    }
}
