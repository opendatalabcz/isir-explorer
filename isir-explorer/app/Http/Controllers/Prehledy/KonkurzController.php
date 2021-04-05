<?php

namespace App\Http\Controllers\Prehledy;

use App\Http\Controllers\Stats\OsobaController;
use App\Http\Controllers\Stats\PocetInsController;
use Illuminate\Http\Request;

class KonkurzController extends BasePrehledController
{
    public const TYP_RIZENI = 'K';

    public function index(Request $request){
        $viewData = [];

        $viewData['pocetNovychMes'] = PocetInsController::pocetNovychInsPoMesicich([
            'typ' => static::TYP_RIZENI,
            'rok' => static::ROK_PRO_PREHLEDY,
        ]);

        $viewData['pocetNovychRoky'] = PocetInsController::pocetNovychInsPoMesicich([
            'typ' => static::TYP_RIZENI,
            'poLetech' => 1,
        ]);

        $viewData['typOsoby'] = OsobaController::typOsoby([
            'typ' => static::TYP_RIZENI,
        ]);

        $viewData['vekDluznika'] = OsobaController::vekDluznika([
            'typ' => static::TYP_RIZENI,
        ]);

        return view('prehledy.konkurz', $viewData);
    }
}
