<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class PohledavkyController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    const VYCHOZI_ROZSAH = 2;
    const ROZSAH_ZOBRAZENI = [
        0 => ['nazev' => 'Výchozí nastavení'],
        1 => ['nazev' => '0 až 100 milionů Kč', 'max' => 100000000, 'res' => 100000, 'def' => 500000],
        2 => ['nazev' => '0 až 10 milionů Kč', 'max' => 10000000, 'res' => 10000, 'def' => 500000],
        3 => ['nazev' => '0 až 1 milion Kč', 'max' => 1000000, 'res' => 5000, 'def' => 20000],
        4 => ['nazev' => '0 až 300 tisíc Kč', 'max' => 300000, 'res' => 1000, 'def' => 10000],
    ];

    protected static function aplikovatDefiniciRozsahu(&$conf, $id){
        if(isset(self::ROZSAH_ZOBRAZENI[$id])){
            $def = self::ROZSAH_ZOBRAZENI[$id];
            $conf['max'] = $def['max'];
            $conf['res'] = $def['res'];
            if(empty($conf['vychoziRozliseni']))
                $conf['vychoziRozliseni'] = $def['def'];
        }
    }

    public static function pohledavkyVyse(array $conf){

        if(!empty($conf['idRozsahu'])){
            self::aplikovatDefiniciRozsahu($conf, $conf['idRozsahu']);
        }

        if(empty($conf['max']) || empty($conf['res'])){
            self::aplikovatDefiniciRozsahu($conf, self::VYCHOZI_ROZSAH);
        }

        $conf = $conf + ['max' => 10000000, 'res' => 10000, 'typPohledavky' => null, 'zobrazeniTyp' => 'log'];
        $filtr = InsRizeni::query()
            ->join('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka');

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        if('N' == $conf['typPohledavky']){
            $attrName = 'celkova_vyse_nezajistenych';
        }else if('Z' == $conf['typPohledavky']){
            $attrName = 'celkova_vyse_zajistenych';
        }else{
            $attrName = 'celkova_vyse';
        }

        $filtr->select('stat_pohledavky.' . $attrName)
            ->where($attrName, '>=', 1)
            ->where($attrName, '<=', $conf['max']);


        $rows = $filtr->get();

        $histogram = self::intervalMode($rows, $conf['res'], 0, $conf['max'], $attrName);
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? $conf['res'];
        $histogram["xtype"] = $conf['zobrazeniTyp'] == "log" ? "log" : "linear";

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Celková výše pohledávek v řízení (Kč)',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public static function pohledavky(array $conf){

        $conf = $conf + ['zobrazeniTyp' => 'log'];

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        $filtr->select('stat_pohledavky.pohledavky_pocet')
            ->join('stat_pohledavky', 'stat_pohledavky.spisovaznacka', '=', 'stat_vec.spisovaznacka')
            ->where('pohledavky_pocet', '>=', 1)
            ->where('pohledavky_pocet', '<=', 200)
            ->whereNotNull('delka_rizeni');

        $rows = $filtr->get();

        $histogram = self::intervalMode($rows, 1, 0, 200, 'pohledavky_pocet');
        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 5;
        $histogram["xtype"] = $conf['zobrazeniTyp'] == "log" ? "log" : "linear";

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Počet přihlášených pohledávek',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public function pohledavky_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Počet pohledávek',
            'jednotkaRozsahu' => 'pohledávek',
            'povolitPrazdneObdobi' => false,
            'extraNastaveni' => ['zobrazeniTyp'],
        ];

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, static::VOLBA_ROK_VYCHOZI),
            'typOsoby' => $this->getTypOsoby($request),
            'zobrazeniTyp' => $request->get("zobrazeniTyp", "linear"),
            'vychoziRozliseni' => 5,
        ]);

        return $this->statView('stats.detail-pohledavky', $viewData);
    }

    public function pohledavkyVyse_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Velikost insolvence',
            'jednotkaRozsahu' => 'Kč',
            'povolitPrazdneObdobi' => false,
            'extraNastaveni' => ['typPohledavky', 'idRozsahu', 'zobrazeniTyp'],
            'rozsahyZobrazeni' => self::ROZSAH_ZOBRAZENI,
        ];

        $viewData['pohledavkyVyse'] = PohledavkyController::pohledavkyVyse([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, static::VOLBA_ROK_VYCHOZI),
            'typOsoby' => $this->getTypOsoby($request),
            'typPohledavky' => $request->get("typPohledavky"),
            'idRozsahu' => $request->get("idRozsahu"),
            'zobrazeniTyp' => $request->get("zobrazeniTyp", "log"),
        ]);

        return $this->statView('stats.detail-pohledavkyVyse', $viewData);
    }

}

