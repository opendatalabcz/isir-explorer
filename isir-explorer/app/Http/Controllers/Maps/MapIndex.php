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
        'stat.mapy.dluznik.vek' => [
            'nazev' => 'Věk dlužníka'
        ],
        'stat.mapy.oddl.uspesnost' => [
            'nazev' => 'Úspěšnost oddlužení'
        ],
        'stat.mapy.oddl.zrusena' => [
            'nazev' => 'Zrušená oddlužení'
        ],
        'stat.mapy.oddl.osvobozeni' => [
            'nazev' => 'Oddlužení – výše osvobození od dluhů'
        ],
        'stat.mapy.oddl.prijmy_dluznika' => [
            'nazev' => 'Oddlužení – příjmy dlužníka'
        ],
    ];

}
