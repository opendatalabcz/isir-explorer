<?php

namespace App\Http\Controllers\Prehledy;

use App\Http\Controllers\Stats\DelkaRizeniController;
use App\Http\Controllers\Stats\OsobaController;
use App\Http\Controllers\Stats\PocetInsController;
use App\Http\Controllers\Stats\PohledavkyController;
use Illuminate\Http\Request;

class ReorgController extends BasePrehledController
{
    public const TYP_RIZENI = 'R';

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
            'vychoziRozliseni' => 5,
        ]);

        $viewData['delkaRizeni'] = DelkaRizeniController::delkaRizeni([
            'typ' => static::TYP_RIZENI,
            'vychoziRozliseni' => 12,
        ]);

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'typ' => static::TYP_RIZENI,
            'vychoziRozliseni' => 5,
        ]);

        return view('prehledy.reorg', $viewData);
    }
}
