@extends('stats.base')

@section('graf')

<div class="chartBox sm" id="el_formaOddluzeni"></div>

<script>
var formaOddluzeni_json = '{!!  json_encode($formaOddluzeni) !!}';

window.addEventListener("load", function(){
    google.charts.load('current', {
        packages: ['corechart', 'bar'],
        'language': 'cs',
    });
    google.charts.setOnLoadCallback(drawCharts);
});

function drawCharts(){
    formaOddluzeni('el_formaOddluzeni', formaOddluzeni_json);
}
</script>

@endsection
