<?php

namespace App\Http\Controllers;

use App\Models\Spravce;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class VeriteleController extends Controller
{

    public const TYP_ZOBRAZENI = [
        'pocty-insolvenci' => [
            'nazev' => 'Počty insolvencí'
        ],
    ];

    public function list(Request $request){

        $veritele = DB::table('stat_spravce')
            ->where('posledni_ins', '>=', '2019-01-01')
            ->orderBy('nazev','ASC')
            ->get();

        $zobrazeni = $request->get('zobrazeni');


        return view('veritele.list', [
            'spravci' => $veritele,
            'zobrazeni' => $zobrazeni,
        ]);
    }

}
