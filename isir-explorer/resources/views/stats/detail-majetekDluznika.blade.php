@extends('stats.base')

@section('graf')

<div id="el_majetekDluznika"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var majetekDluznika_json = '{!!  json_encode($majetekDluznika) !!}';

window.addEventListener("load", function(){
    histogram('el_majetekDluznika', majetekDluznika_json);
});
</script>

@endsection
