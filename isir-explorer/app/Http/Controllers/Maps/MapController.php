<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Controller;
use App\Models\InsRizeni;
use App\Models\Statistiky;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

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

    protected $obdobi;

    protected function koncovaDataObdobi(string $obdobi){
        $rozmezi = new \stdClass;

        if(strlen($obdobi) == 4){
            $rok = (int)$obdobi;
            $date = Carbon::createFromDate($rok, 1, 1);
            $rozmezi->od = $date->copy()->startOfYear();
            $rozmezi->do = $date->copy()->endOfYear();
        }else{
            $parts = explode("/", $obdobi);
            $rok = (int)$parts[0];
            $mesic = (int)$parts[1];
            $date = Carbon::createFromDate($rok, $mesic, 1);
            $rozmezi->od = $date->copy()->startOfMonth();
            $rozmezi->do = $date->copy()->endOfMonth();
        }

        return $rozmezi;
    }

    protected function vyberObdobi(){
        $res = [];
        $now = Carbon::now();
        $date = Carbon::createFromDate(2019, 1, 1);

        while($date < $now){
            if($date->month == 1){
                $res[] = $date->year;
            }
            $res[] = $date->year . "/" . str_pad($date->month, 2, '0', STR_PAD_LEFT);
            $date->addMonth();
        }

        return $res;
    }

    public function kraje(Request $request){
        $geojson = file_get_contents(resource_path('geodata/kraje.min.geojson'));
        $kraje = json_decode($geojson, true);

        // add cache
        return response()->json($kraje);
    }

    protected function filtrParamTypOsoby(Request $request, $filtr){
        if($request->has("typOsoby")){
            $typOsoby = $request->get("typOsoby");
            if("FN" == $typOsoby){
                $filtr->where('typ_osoby', '=', 'F')
                      ->where('podnikatel', '=', false);
            }else if("FP" == $typOsoby){
                $filtr->where('typ_osoby', '=', 'F')
                      ->where('podnikatel', '=', true);
            }else if("P" == $typOsoby){
                $filtr->where('typ_osoby', '=', 'P');
            }
        }
    }

    protected function filtrParamZpusobReseni(Request $request, $filtr){
        if($request->has("zpusobReseni")){
            $zpusobReseni = $request->get("zpusobReseni");
            $filtr->where('typ_rizeni', '=', $zpusobReseni);
        }
    }

    protected function filtrParamObdobi(Request $request, $filtr){
        if($request->has("obdobi")){
            $obdobi = $request->get("obdobi");
        }else{
            $obdobi = "2019";
        }

        $obdobi = $this->koncovaDataObdobi($obdobi);

        $filtr
            ->where('datum_zahajeni', '>=', $obdobi->od)
            ->where('datum_zahajeni', '<=', $obdobi->do);

        $this->obdobi = $obdobi;
    }

    protected function mapView($data){

        $data = $data + [
            'nazvyKraju' => self::KRAJE,
            'nazevHodnoty' => '?',
            'nazevMapy' => '?',
            'varianty' => $this->vyberObdobi(),
            'obdobi' => $this->obdobi,
            'poznamky' => [],
        ];

        if(empty($data['nazevHodnotyInfobox']))
            $data['nazevHodnotyInfobox'] = $data['nazevHodnoty'];

        return view('mapy.map-view', $data);
    }
}
