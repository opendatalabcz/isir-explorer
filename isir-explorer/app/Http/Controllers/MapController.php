<?php

namespace App\Http\Controllers;

use App\Models\Statistiky;
use Illuminate\Http\Request;

class MapController extends Controller
{

    public const KRAJE = [
        'PR' => 'Praha',
        'JC' => 'Jihočeský kraj',
        'JM' => 'Jihomoravský kraj',
        'KA' => 'Karlovarský kraj',
        'VY' => 'Kraj Vysočina',
        'KR' => 'Královéhradecký kraj',
        'LI' => 'Liberecký kraj',
        'MO' => 'Moravskoslezský kraj',
        'OL' => 'Olomoucký kraj',
        'PA' => 'Pardubický kraj',
        'PL' => 'Plzeňský kraj',
        'ST' => 'Středočeský kraj',
        'US' => 'Ústecký kraj',
        'ZL' => 'Zlínský kraj',
    ];

    public function insolvence(Request $request){
        if($request->has("rok")){
            $rok = $request->get("rok");
            $mesic = $request->get("mesic");
        }else{
            $rok = 2019;
            $mesic = null;
        }

        $varianty = Statistiky::where('nazev','=','mapy.kraje.ins')->orderBy('rok','ASC')->orderBy('mesic', 'ASC')->get();

        $datarow = Statistiky::where('nazev','=','mapy.kraje.ins')
            ->where('rok','=',$rok)
            ->where('mesic','=',$mesic)
            ->first();

        if(!$datarow) abort(404);

        $data = $datarow->data;
        $data = json_decode($data, true);

        return view('maps', [
            'data' => $data,
            'nazvyKraju' => self::KRAJE,
            'nazevHodnoty' => 'Insolvencí',
            'nazevMapy' => 'Počet insolvencí dle krajů',
            'varianty' => $varianty,
            'datarow' => $datarow,
        ]);
    }

    public function insolvence_na_obyvatele(Request $request){
    }


    public function kraje(Request $request){
        $geojson = file_get_contents(resource_path('geodata/kraje.min.geojson'));
        $kraje = json_decode($geojson, true);

        // add cache
        return response()->json($kraje);
    }
}
