<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use App\Models\Veritel;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class VeriteleController extends SubjektController
{

    public const TYP_ZOBRAZENI = [
        'pocty-insolvenci' => [
            'nazev' => 'Počty insolvencí'
        ],
        'vyse-pohledavek' => [
            'nazev' => 'Výše pohledávek'
        ],
        'vyse-zaj-pohledavek' => [
            'nazev' => 'Výše zajištěných pohledávek'
        ],
        'prumerna-vyse-pohledavky' => [
            'nazev' => 'Průměrná výše pohledávky'
        ],
        'pohledavek-v-prihlasce' => [
            'nazev' => 'Počet pohledávek v přihlášce'
        ],
    ];

    public function list(Request $request){

        $zobrazeni = $request->get('zobrazeni');

        if($zobrazeni == 'vyse-pohledavek'){
            $veritele = DB::table('stat_veritel')
                ->orderBy('vyse_celkem','DESC')
                ->whereNotNull('vyse_celkem');
        } else if($zobrazeni == 'prumerna-vyse-pohledavky'){
            $veritele = DB::table('stat_veritel')
                ->orderByRaw('(vyse_celkem/prihlasky_pocet) DESC')
                ->where('prihlasky_pocet', '>', 10)
                ->where('vyse_celkem', '>', 0)
                ->whereNotNull('vyse_celkem');
        } else if($zobrazeni == 'vyse-zaj-pohledavek'){
            $veritele = DB::table('stat_veritel')
                ->orderBy('vyse_zaj','DESC')
                ->where('vyse_zaj', '>', 0)
                ->whereNotNull('vyse_zaj');
        } else if($zobrazeni == 'pohledavek-v-prihlasce'){
            $veritele = DB::table('stat_veritel')
                ->orderByRaw('(pohledavky_pocet/prihlasky_pocet) DESC')
                ->where('prihlasky_pocet', '>', 10)
                ->where('pohledavky_pocet', '>', 0);
        }else{
            $zobrazeni = 'pocty-insolvenci';
            $veritele = DB::table('stat_veritel')
                ->orderBy('ins_celkem','DESC')
                ->whereNotNull('ins_celkem');
        }

        $veritele = $veritele->limit(1000)->get();

        return view('veritele.list', [
            'veritele' => $veritele,
            'zobrazeni' => $zobrazeni,
        ]);
    }

    protected function miraPrecteniUdaju($veritel){

        $res =  [
            'celkem' => $veritel->ins_celkem ?? 0,
            'pp' => $veritel->prihlasky_pocet ?? 0,
            'mira' => 0,
        ];
        if($res['celkem']){
            $res['mira'] = $res['pp'] / ($res['celkem'] / 100);
        }
        return $res;
    }

    public function detail($id, Request $request){

        $veritel = Veritel::where('id','=',$id)->first();

        if(!$veritel)
            abort(404);

        $insRizeni = $veritel->rizeni->sortByDesc('datum_zahajeni');

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

        return view('veritele.detail', [
            'veritel' => $veritel,
            'kraje' => $kraje,
            'info' => $info,
            'ins_stats' => $this->typyRizeniSubjektu($id, self::TYP_VERITEL),
            'mira_precteni' => $this->miraPrecteniUdaju($veritel),
            /*'ins_stats' => $this->typyRizeniSpravce($id),
            'odmeny' => $this->odmenySpravce($id),
            'oddluzeni' => $this->posledniOddluzeni($id),
            'mira_precteni' => $this->miraPrecteniUdaju($id),*/
        ]);

    }

}
