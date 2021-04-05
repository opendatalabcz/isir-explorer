@extends('stats.base')

@section('graf')

<div class="chartBox sm" id="el_typyOsob"></div>

<script>
var typyOsob_json = '{!!  json_encode($typOsoby) !!}';

window.addEventListener("load", function(){
    google.charts.load('current', {
        packages: ['corechart', 'bar']
    });
    google.charts.setOnLoadCallback(drawCharts);
});

function drawCharts(){
    typOsoby('el_typyOsob', typyOsob_json);
}
</script>

@endsection
