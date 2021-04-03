<?php

namespace App\Http\Controllers\Maps;

use App\Http\Controllers\Controller;


class MapIndex extends Controller
{

    public const MAPY = [
        'stat.mapy.ins' => [
            'nazev' => 'Počty insolvencí'
        ],
        'stat.mapy.ins.obyv' => [
            'nazev' => 'Míra populace v insolvenci'
        ],
        'stat.mapy.pohledavky' => [
            'nazev' => 'Výše přihlášených pohledávek'
        ],
    ];

}