@extends('stats.base')

@section('graf')

<div class="chartBox detail" id="el_pocetNovychIns"></div>

<script>
var pocetNovychIns_json = '{!!  json_encode($pocetNovych) !!}';

window.addEventListener("load", function(){
    google.charts.load('current', {
        packages: ['corechart', 'bar']
    });
    google.charts.setOnLoadCallback(drawCharts);
});

function drawCharts(){
    pocetNovychIns('el_pocetNovychIns', pocetNovychIns_json);
}
</script>

@endsection
