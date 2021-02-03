<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class MapController extends Controller
{
    public function kraje(Request $request){
        $data = '{"OL": 1896, "KR": 2064, "JC": 1720, "LI": 1594, "PL": 1721, "PR": 3113, "ZL": 1266, "ST": 2950, "JM": 3247, "MO": 4664, "KA": 950, "US": 4270, "VY": 1514, "PA": 2292}';
        $data = json_decode($data, true);

        $geojson = file_get_contents(resource_path('geodata/kraje.min.geojson'));
        $kraje = json_decode($geojson, true);
        foreach ($kraje["features"] as &$ftr) {
            $kodKraje = $ftr["properties"]["ref"];
            $ftr["properties"]["ins"] = $data[$kodKraje];
        }
        // add
        return response()->json($kraje);
    }
}
