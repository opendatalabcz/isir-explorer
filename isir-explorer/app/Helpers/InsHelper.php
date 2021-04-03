<?php

function getInsLink($spis) {
    if(!$spis) return "#";
    $parts = explode(" ", $spis, 2);
    $rocnikVec = explode("/", $parts[1], 2);
    return "https://isir.justice.cz/isir/ueu/vysledek_lustrace.do?bc_vec=" . $rocnikVec[0] . "&rocnik=" . $rocnikVec[1] . "&aktualnost=AKTUALNI_I_UKONCENA";
}

function getInsDocLink($id) {
    return "https://isir.justice.cz:8443/isir_public_ws/doc/Document?idDokument=" . $id;
}

function formatKc($number){
    return number_format($number, 2, ',', ' ');
}

function setUriParam(array $query){
    $r = request();
    $question = $r->getBaseUrl().$r->getPathInfo() === '/' ? '/?' : '?';

    if(count($r->query()) > 0){
        $query = array_merge($r->query(), $query);
        unset($query["page"]);
        return $r->url().$question.\Illuminate\Support\Arr::query($query);
    }else{
        return $r->fullUrl().$question.\Illuminate\Support\Arr::query($query);
    }
}
