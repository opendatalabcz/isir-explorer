<?php

namespace App\Http\Controllers;

use App\Models\InsRizeni;
use App\Models\Statistiky;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class StatController extends Controller
{

    public function insolvence(Request $request){
        if($request->has("rok")){
            $rok = $request->get("rok");
            $mesic = $request->get("mesic");
        }else{
            $rok = 2019;
            $mesic = null;
        }

        $datarow = Statistiky::where('nazev','=','stat.pocet.ins')
            ->where('rok','=',$rok)
            ->where('mesic','=',$mesic)
            ->first();

        if(!$datarow) abort(404);

        $data = $datarow->data;
        $data = json_decode($data, true);

        return view('ins', [
            'data' => $data,
            'datarow' => $datarow,
        ]);
    }
}
