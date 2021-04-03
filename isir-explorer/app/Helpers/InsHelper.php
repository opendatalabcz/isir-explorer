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
