<?php

namespace App\Http\Controllers\Prehledy;

use App\Http\Controllers\Stats\DelkaRizeniController;
use App\Http\Controllers\Stats\OsobaController;
use App\Http\Controllers\Stats\PocetInsController;
use App\Http\Controllers\Stats\PohledavkyController;
use Illuminate\Http\Request;

class InsController extends BasePrehledController
{

    public function index(Request $request){
        $viewData = [];

        $viewData['pocetNovychMes'] = PocetInsController::pocetNovychInsPoMesicich([
            'rok' => static::ROK_PRO_PREHLEDY,
        ]);

        $viewData['pocetNovychRoky'] = PocetInsController::pocetNovychInsPoMesicich([
            'poLetech' => 1,
        ]);

        $viewData['typOsoby'] = OsobaController::typOsoby([
        ]);

        $viewData['vekDluznika'] = OsobaController::vekDluznika([
            'vychoziRozliseni' => 5,
        ]);

        $viewData['delkaRizeni'] = DelkaRizeniController::delkaRizeni([
            'rok' => 2010,
            'vychoziRozliseni' => 12,
        ]);

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'rok' => 2019,
            'vychoziRozliseni' => 5,
        ]);

        $viewData['pohledavkyVyseCelkem'] = PohledavkyController::pohledavkyVyse([
            'rok' => 2019,
            'idRozsahu' => 2,
            'vychoziRozliseni' => 1000000,
        ]);

        $viewData['pohledavkyVyseZaji'] = PohledavkyController::pohledavkyVyse([
            'rok' => 2019,
            'typPohledavky' => 'Z',
            'idRozsahu' => 2,
            'vychoziRozliseni' => 1000000,
        ]);

        return view('prehledy.ins', $viewData);
    }
}
