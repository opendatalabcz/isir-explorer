<?php

namespace App\Http\Controllers\Prehledy;

use App\Http\Controllers\Stats\DelkaRizeniController;
use App\Http\Controllers\Stats\OddlFormaController;
use App\Http\Controllers\Stats\OddlMajetekController;
use App\Http\Controllers\Stats\OddlMiraUspokojeniController;
use App\Http\Controllers\Stats\OddlPrijmyController;
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
            'vychoziRozliseni' => 1,
        ]);

        $viewData['delkaRizeni'] = DelkaRizeniController::delkaRizeni([
            'typ' => static::TYP_RIZENI,
            'vychoziRozliseni' => 1,
        ]);

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'typ' => static::TYP_RIZENI,
            'vychoziRozliseni' => 2,
        ]);

        $viewData['pohledavkyVyseCelkem'] = PohledavkyController::pohledavkyVyse([
            'typ' => static::TYP_RIZENI,
            'idRozsahu' => 2,
        ]);

        $viewData['pohledavkyVyseZaji'] = PohledavkyController::pohledavkyVyse([
            'typ' => static::TYP_RIZENI,
            'typPohledavky' => 'Z',
            'idRozsahu' => 2,
        ]);

        $viewData['miraUspokojeni'] = OddlMiraUspokojeniController::miraUspokojeni([
            'miraUspokojeni' => OddlMiraUspokojeniController::ZOBRAZ_MIRA_SKUTECNA,
            'zobrazeniTyp' => 'lin',
            'vychoziRozliseni' => 1,
        ]);

        $viewData['miraUspokojeniRozdil'] = OddlMiraUspokojeniController::miraUspokojeni([
            'miraUspokojeni' => OddlMiraUspokojeniController::ZOBRAZ_MIRA_ROZDIL,
            'zobrazeniTyp' => 'log',
            'vychoziRozliseni' => 4,
        ]);

        $viewData['prijmyDluznika'] = OddlPrijmyController::prijmyDluznika([
            'vychoziRozliseni' => 1000,
        ]);

        $viewData['majetekDluznika'] = OddlMajetekController::majetekDluznika([
            'zobrazeniTyp' => 'log',
            'idRozsahu' => 3,
            'vychoziRozliseni' => 10000,
        ]);

        $viewData['formaOddluzeniIS'] = OddlFormaController::formaOddluzeni([
            'navrhujiciStrana' => 'IS',
        ]);

        $viewData['formaOddluzeniDL'] = OddlFormaController::formaOddluzeni([
            'navrhujiciStrana' => 'DL',
        ]);

        return view('prehledy.oddluzeni', $viewData);
    }
}
