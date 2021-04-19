<?php
namespace App\Http\Controllers\Stats;

trait StatsFilters {

    protected static function filtrObdobi($filtr, $conf){
        if(!empty($conf['rok'])){
            $filtr->where('zahajeni_r', '=', $conf['rok']);
        }
    }

    protected static function filtrObdobiUkonceni($filtr, $conf){
        if(!empty($conf['rok'])){
            $filtr->where('ukonceni_r', '=', $conf['rok']);
        }
    }

    protected static function filtrZpusobReseni($filtr, $conf){
        if(!empty($conf['typ'])){
            $filtr->where('typ_rizeni', '=', $conf['typ']);
        }
    }

    protected static function filtrTypOsoby($filtr, $conf){
        $typOsoby = $conf['typOsoby'] ?? null;
        if("FN" == $typOsoby){
            $filtr->where('typ_osoby', '=', 'F')
                    ->where('podnikatel', '=', false);
        }else if("FP" == $typOsoby){
            $filtr->where('typ_osoby', '=', 'F')
                    ->where('podnikatel', '=', true);
        }else if("P" == $typOsoby){
            $filtr->where('typ_osoby', '=', 'P');
        }
    }

    public static function nazevTypuOsoby($row){
        if($row['typ_osoby'] == "P")
            return "Právnická";
        else if($row['typ_osoby'] == "F" && false === $row['podnikatel'])
            return "Fyzická - nepodnikatel";
        else if($row['typ_osoby'] == "F" && true === $row['podnikatel'])
            return "Fyzická - podnikatel";
        return null;
    }

}
