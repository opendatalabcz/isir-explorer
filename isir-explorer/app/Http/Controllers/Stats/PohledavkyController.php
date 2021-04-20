<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;

class PohledavkyController extends StatsController
{
    use StatsFilters;
    protected static $celkemPocetIns = 0;

    const VYCHOZI_ROZSAH = 2;

    public static function pohledavkyVyse(array $conf){
        $conf = $conf + ['typPohledavky' => null, 'zobrazeniTyp' => 'logxy'];

        if(!empty($conf['idRozsahu'])){
            self::aplikovatDefiniciRozsahu($conf, $conf['idRozsahu']);
        }

        if(empty($conf['max']) || empty($conf['res'])){
            self::aplikovatDefiniciRozsahu($conf, self::VYCHOZI_ROZSAH);
        }

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
        self::aplikovatNastaveniOs($histogram, $conf);
        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Celková výše pohledávek v řízení (Kč)',
                'y' => 'Počet insolvencí',
            ],
        ];
    }

    public static function pohledavky(array $conf){

        $conf = $conf + ['zobrazeniTyp' => 'logxy'];

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
        self::aplikovatNastaveniOs($histogram, $conf);

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
            'povolitPrazdneObdobi' => true,
            'extraNastaveni' => ['zobrazeniTyp'],
            'vychoziZobrazeniTyp' => 'logxy',
        ];

        $viewData['pohledavky'] = PohledavkyController::pohledavky([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request),
            'typOsoby' => $this->getTypOsoby($request),
            'zobrazeniTyp' => $request->get("zobrazeniTyp", "logxy"),
            'vychoziRozliseni' => 2,
        ]);

        return $this->statView('stats.detail-pohledavky', $viewData);
    }

    public function pohledavkyVyse_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Velikost insolvence',
            'jednotkaRozsahu' => 'Kč',
            'povolitPrazdneObdobi' => true,
            'extraNastaveni' => ['typPohledavky', 'idRozsahu', 'zobrazeniTyp'],
            'rozsahyZobrazeni' => self::ROZSAH_ZOBRAZENI,
            'vychoziZobrazeniTyp' => 'logxy',
        ];

        $viewData['pohledavkyVyse'] = PohledavkyController::pohledavkyVyse([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request),
            'typOsoby' => $this->getTypOsoby($request),
            'typPohledavky' => $request->get("typPohledavky"),
            'idRozsahu' => $request->get("idRozsahu"),
            'zobrazeniTyp' => $request->get("zobrazeniTyp", "logxy"),
        ]);

        return $this->statView('stats.detail-pohledavkyVyse', $viewData);
    }

}

