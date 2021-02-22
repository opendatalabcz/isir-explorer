<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use Carbon\Carbon;
use Illuminate\Http\Request;

class SpravciController extends Controller
{

    public function list(Request $request){

        $spravci = Spravce::orderBy('nazev','ASC')->get();

        return view('spravci.list', [
            'spravci' => $spravci,
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
        ]);

    }

}
