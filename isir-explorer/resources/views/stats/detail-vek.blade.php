@extends('stats.base')

@section('graf')

<div id="el_vekDluznika"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var vekDluznika_json = '{!!  json_encode($vekDluznika) !!}';

window.addEventListener("load", function(){
    histogram('el_vekDluznika', vekDluznika_json);
});
</script>

@endsection
