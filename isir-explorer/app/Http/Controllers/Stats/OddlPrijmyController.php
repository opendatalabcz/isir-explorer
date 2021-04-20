<?php

namespace App\Http\Controllers\Stats;

use App\Models\InsRizeni;
use Illuminate\Http\Request;

class OddlPrijmyController extends StatsController
{
    use StatsFilters;

    public const TYP_PRIJMU = [
        0 => ['isir' => null, 'nazev' => 'Celkový příjem dlužníka'],
        1 => ['isir' => '1. mzda a plat', 'nazev' => 'Mzda a plat'],
        2 => ['isir' => '1. darovací smlouva', 'nazev' => 'Darovací smlouva'],
        3 => ['isir' => '2. smlouva o důchodu', 'nazev' => 'Smlouva o důchodu'],
        4 => ['isir' => '5. starobní a jiný důchod', 'nazev' => 'Starobní a jiný důchod'],
        5 => ['isir' => '4. příjmy ze samostatné činnosti', 'nazev' => 'Příjmy ze samostatné činnosti'],
        6 => ['isir' => '3. dohoda o provedení práce', 'nazev' => 'Dohoda o provedení práce'],
        7 => ['isir' => '2. dohoda o pracovní činnosti', 'nazev' => 'Dohoda o pracovní činnosti'],
        8 => ['isir' => '6. výsluhový příspěvek', 'nazev' => 'Výsluhový příspěvek'],
        9 => ['isir' => '7. cestovní náhrady a zahraniční stravné', 'nazev' => 'Cestovní náhrady a zahraniční stravné'],
        10 => ['isir' => '8. jiný příjem', 'nazev' => 'Jiný příjem'],
    ];

    public static function prijmyDluznika(array $conf){

        $conf = $conf + ['zobrazeniTyp' => 'linear', 'typPrijmu' => 0];

        $filtr = InsRizeni::query();

        self::filtrObdobi($filtr, $conf);
        self::filtrZpusobReseni($filtr, $conf);
        self::filtrTypOsoby($filtr, $conf);

        $filtr->join('stat_oddluzeni', 'stat_oddluzeni.spisovaznacka', '=', 'stat_vec.spisovaznacka')
              ->join('zprava_pro_oddluzeni', 'zprava_pro_oddluzeni.id', '=', 'stat_oddluzeni.zpro_id');

        if( 0 == $conf['typPrijmu'] ){
            $filtr->select('prijmy_celkem')
                ->where('prijmy_celkem', '>=', 0);
        }else{
            if(empty(self::TYP_PRIJMU[$conf['typPrijmu']]))
                abort(404);
            $prijemTyp = self::TYP_PRIJMU[$conf['typPrijmu']];
            $filtr->select('vyse AS prijmy_celkem')
                ->join('zpro_prijem_dluznika', 'zpro_prijem_dluznika.zpro_id', '=', 'stat_oddluzeni.zpro_id')
                ->where('typ', '=', $prijemTyp['isir'])
                ->where('prijmy_celkem', '>=', 0);
        }

        $rows = $filtr->get();
        $histogram = self::intervalMode($rows, 1000, 0, 100000, 'prijmy_celkem');

        $histogram["defRes"] = $conf['vychoziRozliseni'] ?? 1;
        $histogram["ytype"] = $conf['zobrazeniTyp'] == "log" ? "log" : "linear";

        return [
            'data' => $histogram,
            'labels' => [
                'x' => 'Čisté měsíční příjmy (Kč)',
                'y' => 'Počet dlužníků',
            ],
        ];
    }

    public function prijmyDluznika_detail(Request $request){
        $viewData = [
            'nazevStatistiky' => 'Oddlužení – příjmy dlužníka',
            'jednotkaRozsahu' => 'Kč',
            'povolitPrazdneObdobi' => true,
            'nastaveni' => ['obdobi', 'typOsoby'],
            'extraNastaveni' => ['zobrazeniTyp', 'typPrijmu'],
            'vyraditTypOsoby' => ['P'],
            'poznamky' => [
                'Zahrnuta jsou data pouze z insolvenčních řízení, pro která se podařilo přečíst data o příjmech dlužníka ze Zprávy pro oddlužení.'
            ],
        ];

        $viewData['prijmyDluznika'] = self::prijmyDluznika([
            'typ' => $this->getZpusobReseni($request),
            'rok' => $this->getRok($request, null),
            'typOsoby' => $this->getTypOsoby($request),
            'vychoziRozliseni' => 1000,
            'zobrazeniTyp' => $request->get("zobrazeniTyp"),
            'typPrijmu' => intval($request->get("typPrijmu", 0)),
        ]);

        return $this->statView('stats.detail-prijmyDluznika', $viewData);
    }

}

