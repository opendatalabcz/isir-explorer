<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Stats\StatsController;
use Illuminate\Http\Request;

class MapController extends StatsController
{

    /**
     * Zkratky krajů a jejich názvy
     */
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

    protected const VOLBA_ROK_MIN = 2010;
    protected const VOLBA_ROK_VYCHOZI = 2020;
    protected const VOLBA_ROK_MAX = 2021;


    public function kraje(Request $request){
        $geojson = file_get_contents(resource_path('geodata/kraje.min.geojson'));
        $kraje = json_decode($geojson, true);

        // add cache
        return response()->json($kraje);
    }

    protected function mapView($data){
        $data = $data + [
            'vyberPoMesicich' => false,
        ];
        $data = $data + [
            'nazvyKraju' => self::KRAJE,
            'nazevHodnoty' => '?',
            'nazevMapy' => '?',
            'varianty' => $this->vyberObdobi($data['vyberPoMesicich'] ?? true),
            'obdobi' => $this->obdobi,
            'poznamky' => [],
            'inverze' => false, // true pokud je vyssi hodnota metriky prizniva (otocit barvy)
            'jeCastka' => false,
            'nazevVolbyObdobi' => null,
            'nastaveni' => ['obdobi', 'typOsoby', 'insZpusob'],
            'vyraditTypOsoby' => [],
            'extraNastaveni' => [],
        ];

        if(empty($data['nazevHodnotyInfobox']))
            $data['nazevHodnotyInfobox'] = $data['nazevHodnoty'];

        return view('mapy.map-view', $data);
    }
}
