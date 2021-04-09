<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class SpravciController extends Controller
{

    public const TYP_ZOBRAZENI = [
        'pocty-insolvenci' => [
            'nazev' => 'Počty insolvencí'
        ],
        'velikosti-insolvenci' => [
            'nazev' => 'Velikosti insolvencí'
        ],
        'evidovana-odmena' => [
            'nazev' => 'Evidovaná odměna'
        ],
        'prumerna-odmena' => [
            'nazev' => 'Průměrná odměna'
        ],
    ];

    public function list(Request $request){

        $spravci_rows = DB::table('stat_spravce')
            ->where('posledni_ins', '>=', '2019-01-01')
            ->orderBy('nazev','ASC')
            ->get();
        $spravci = [];
        foreach ($spravci_rows as $value) {
            $spravci[$value->id] = $value;
        }

        $zobrazeni = $request->get('zobrazeni');

        if('velikosti-insolvenci' == $zobrazeni){
            $dataSpravcu = DB::table('stat_spravce')
                ->where('posledni_ins', '>=', '2019-01-01')
                ->join('stat_spravce_ins', 'stat_spravce_ins.id_spravce', '=', 'stat_spravce.id')
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
                ->join('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->select(
                    'stat_spravce.id',
                    DB::raw('count(*) as pocet'),
                    DB::raw('sum(celkova_vyse) as celkova_vyse'),
                    DB::raw('sum(pohledavky_pocet) as pohledavky_pocet'),
                )
                ->groupBy('stat_spravce.id')
                ->get();
            foreach ($dataSpravcu as $value) {
                $spravci[$value->id]->agreagace = $value;
            }
        }else if('evidovana-odmena' == $zobrazeni){
            $zobrazeni = 'evidovana-odmena';
            $dataSpravcu = DB::table('stat_spravce')
                ->where('posledni_ins', '>=', '2019-01-01')
                ->join('stat_spravce_ins', 'stat_spravce_ins.id_spravce', '=', 'stat_spravce.id')
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
                ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->join('zspo_odmena_spravce', 'zspo_odmena_spravce.zspo_id', '=', 'stat_oddluzeni.zspo_id')

                ->select(
                    'stat_spravce.id',
                    DB::raw('count(*) as pocet'),
                    DB::raw('sum(zspo_odmena_spravce.celkova_odmena) as celkova_odmena'),
                    DB::raw('sum(hotove_vydaje) as hotove_vydaje'),
                )
                ->groupBy('stat_spravce.id')
                ->get();
            foreach ($dataSpravcu as $value) {
                $spravci[$value->id]->agreagace = $value;
            }
            foreach ($spravci as $id => $value) {
                if(!property_exists($spravci[$id], 'agreagace'))
                    unset($spravci[$id]);
            }
        }else if('prumerna-odmena' == $zobrazeni){
            $zobrazeni = 'prumerna-odmena';
            $dataSpravcu = DB::table('stat_spravce')
                ->where('posledni_ins', '>=', '2019-01-01')
                ->join('stat_spravce_ins', 'stat_spravce_ins.id_spravce', '=', 'stat_spravce.id')
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
                ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->join('zspo_odmena_spravce', 'zspo_odmena_spravce.zspo_id', '=', 'stat_oddluzeni.zspo_id')

                ->select(
                    'stat_spravce.id',
                    DB::raw('count(*) as pocet'),
                    DB::raw('sum(zspo_odmena_spravce.celkova_odmena) as celkova_odmena'),
                    DB::raw('sum(hotove_vydaje) as hotove_vydaje'),
                )
                ->groupBy('stat_spravce.id')
                ->get();
            foreach ($dataSpravcu as $value) {
                $spravci[$value->id]->agreagace = $value;
                if($spravci[$value->id]->agreagace->pocet){
                    $spravci[$value->id]->agreagace->celkova_odmena /= $spravci[$value->id]->agreagace->pocet;
                    $spravci[$value->id]->agreagace->hotove_vydaje /= $spravci[$value->id]->agreagace->pocet;
                }else{
                    $spravci[$value->id]->agreagace->celkova_odmena = 0;
                    $spravci[$value->id]->agreagace->hotove_vydaje = 0;
                }
            }
            foreach ($spravci as $id => $value) {
                if(!property_exists($spravci[$id], 'agreagace'))
                    unset($spravci[$id]);
            }
        }else{
            $zobrazeni = 'pocty-insolvenci';
        }

        return view('spravci.list', [
            'spravci' => $spravci,
            'zobrazeni' => $zobrazeni,
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

    protected function odmenySpravce($idSpravce, $limit = 10){
        $odmenySpravce = DB::table('stat_spravce_ins')
                ->where('stat_spravce_ins.id_spravce', '=', $idSpravce)
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
                ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->join('zspo_odmena_spravce', 'stat_oddluzeni.zspo_id', '=', 'zspo_odmena_spravce.zspo_id')
                ->join('dokument', 'dokument.id', '=', 'zspo_odmena_spravce.zspo_id')
                ->select(
                    '*',
                )
                ->whereNotNull('dokument.zverejneni')
                ->orderBy('dokument.zverejneni','DESC')
                ->limit($limit)->get();


        foreach($odmenySpravce as &$odmena){
            $celkemOdmena = ($odmena->celkova_odmena ?? 0) + ($odmena->hotove_vydaje ?? 0);
            $celkemUhrazeno = ($odmena->celkova_odmena_uhrazeno ?? 0) + ($odmena->hotove_vydaje_uhrazeno ?? 0);
            if(empty($celkemOdmena))
                $odmena->uhrazeno = 100;
            else
                $odmena->uhrazeno = ($celkemUhrazeno / $celkemOdmena) * 100;
        }

        return $odmenySpravce;
    }

    protected function posledniOddluzeni($idSpravce, $limit = 10){
        $odmenySpravce = DB::table('stat_spravce_ins')
                ->where('stat_spravce_ins.id_spravce', '=', $idSpravce)
                ->where('stat_pohledavky.celkova_vyse', '>', 0)
                ->join('stat_vec', 'stat_vec.id', '=', 'stat_spravce_ins.id_ins')
                ->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->leftJoin('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka')
                ->join('zspo_odmena_spravce', 'stat_oddluzeni.zspo_id', '=', 'zspo_odmena_spravce.zspo_id')
                ->join('dokument', 'dokument.id', '=', 'zspo_odmena_spravce.zspo_id')
                ->select(
                    '*', DB::raw('stat_vec.spisovaznacka as spisovaznacka')
                )
                ->whereNotNull('dokument.zverejneni')
                ->orderBy('dokument.zverejneni','DESC')
                ->limit($limit)->get();


        foreach($odmenySpravce as &$odmena){
            $celkemOdmena = ($odmena->celkova_odmena ?? 0) + ($odmena->hotove_vydaje ?? 0);
            $celkemUhrazeno = ($odmena->celkova_odmena_uhrazeno ?? 0) + ($odmena->hotove_vydaje_uhrazeno ?? 0);
            if(empty($celkemOdmena))
                $odmena->uhrazeno = 100;
            else
                $odmena->uhrazeno = ($celkemUhrazeno / $celkemOdmena) * 100;
        }

        return $odmenySpravce;
    }

    public function odmeny($id, Request $request){

        $spravce = Spravce::where('id','=',$id)->first();

        if(!$spravce)
            abort(404);

        return view('spravci.odmeny', [
            'spravce' => $spravce,
            'odmeny' => $this->odmenySpravce($id, 1000),
        ]);
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
            'oddluzeni' => $this->posledniOddluzeni($id),
        ]);

    }

}
