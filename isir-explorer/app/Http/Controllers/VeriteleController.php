<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use App\Models\Veritel;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class VeriteleController extends Controller
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

    public function detail($id, Request $request){

        $veritel = Veritel::where('id','=',$id)->first();

        if(!$veritel)
            abort(404);

    }

}
