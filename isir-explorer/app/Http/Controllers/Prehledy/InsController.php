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
            'vychoziRozliseni' => 1,
        ]);

        $viewData['delkaRizeni'] = DelkaRizeniController::delkaRizeni([
            'vychoziRozliseni' => 1,
        ]);

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'zobrazeniTyp' => 'logxy',
            'vychoziRozliseni' => 2,
        ]);

        $viewData['pohledavkyVyseCelkem'] = PohledavkyController::pohledavkyVyse([
            'idRozsahu' => 2,
        ]);

        $viewData['pohledavkyVyseZaji'] = PohledavkyController::pohledavkyVyse([
            'typPohledavky' => 'Z',
            'idRozsahu' => 2,
        ]);

        return view('prehledy.ins', $viewData);
    }
}
