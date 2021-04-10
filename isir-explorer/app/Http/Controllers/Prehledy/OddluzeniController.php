<?php

namespace App\Http\Controllers\Prehledy;

use App\Http\Controllers\Stats\DelkaRizeniController;
use App\Http\Controllers\Stats\OsobaController;
use App\Http\Controllers\Stats\PocetInsController;
use App\Http\Controllers\Stats\PohledavkyController;
use Illuminate\Http\Request;

class OddluzeniController extends BasePrehledController
{
    public const TYP_RIZENI = 'O';

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
            'rok' => 2012,
            'vychoziRozliseni' => 1,
        ]);

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'typ' => static::TYP_RIZENI,
            'rok' => 2019,
            'vychoziRozliseni' => 5,
        ]);

        $viewData['pohledavkyVyseCelkem'] = PohledavkyController::pohledavkyVyse([
            'typ' => static::TYP_RIZENI,
            'rok' => 2019,
            'idRozsahu' => 2,
            'vychoziRozliseni' => 130000,
        ]);

        $viewData['pohledavkyVyseZaji'] = PohledavkyController::pohledavkyVyse([
            'typ' => static::TYP_RIZENI,
            'rok' => 2019,
            'typPohledavky' => 'Z',
            'idRozsahu' => 2,
            'vychoziRozliseni' => 130000,
        ]);

        return view('prehledy.oddluzeni', $viewData);
    }
}
