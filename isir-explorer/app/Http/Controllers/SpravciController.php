<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class SpravciController extends Controller
{

    public const TYP_ZOBRAZENI = [
        'spravci.ins' => [
            'nazev' => 'Počty insolvencí'
        ],
    ];

    public function list(Request $request){

        $spravci = Spravce::orderBy('nazev','ASC')->get();

        return view('spravci.list', [
            'spravci' => $spravci,
        ]);
    }

    protected function typyRizeniSpravceZaRok($idSpravce, $rok){
        $date = Carbon::createFromDate($rok, 1, 1);
        $od = $date->copy()->startOfYear();
        $do = $date->copy()->endOfYear();

        $typyRizeni = DB::table('stat_spravce_ins')
                ->where('stat_spravce_ins.id_spravce', '=', $idSpravce)
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
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

    protected function typyRizeniSpravce($idSpravce){
        $rok = intval(date("Y"));
        $roky = [$rok-3, $rok-2, $rok-1];
        $result = [];
        foreach ($roky as $rok) {
            $rows = $this->typyRizeniSpravceZaRok($idSpravce, $rok);
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

    protected function odmenySpravce($idSpravce){
        $odmenySpravce = DB::table('stat_spravce_ins')
                ->where('stat_spravce_ins.id_spravce', '=', $idSpravce)
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
                ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->join('zspo_odmena_spravce', 'stat_oddluzeni.zspo_id', '=', 'zspo_odmena_spravce.zspo_id')
                ->join('dokument', 'dokument.id', '=', 'zspo_odmena_spravce.zspo_id')
                ->select(
                    '*'
                )
                //->whereNotNull('dokument.zverejneni')
                //->orderBy('dokument.zverejneni','DESC')
                ->limit(10)->get();
        return $odmenySpravce;
    }

    public function detail($id, Request $request){

        $spravce = Spravce::where('id','=',$id)->first();

        if(!$spravce)
            abort(404);

        $insRizeni = $spravce->rizeni->sortByDesc('datum_zahajeni');

        $info = [
            'zahajeniCinnosti' => $insRizeni->last()->datum_zahajeni,
        ];

        $kraje = [];
        foreach ($insRizeni as $ins) {
            if(!$ins->kraj) continue;
            if(isset($kraje[$ins->kraj]))
                $kraje[$ins->kraj]++;
            else
                $kraje[$ins->kraj] = 1;
        }

        $posledniIns = $insRizeni->take(200);

        $timeline = [];
        foreach ($posledniIns as $ins) {
            $timeline[] = [
                "i" => $ins->spisovaznacka,
                "s" => $ins->datum_zahajeni->timestamp,
                "e" => $ins->datum_ukonceni ? $ins->datum_ukonceni->timestamp : Carbon::now()->timestamp,
                "t" => $ins->typ_rizeni ?? "?",
            ];
        }

        return view('spravci.detail', [
            'spravce' => $spravce,
            'timeline' => $timeline,
            'kraje' => $kraje,
            'info' => $info,
            'ins_stats' => $this->typyRizeniSpravce($id),
            'odmeny' => $this->odmenySpravce($id),
        ]);

    }

}
