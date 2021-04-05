@extends('stats.base')

@section('graf')

<div id="el_delkaRizeni"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var delkaRizeni_json = '{!!  json_encode($delkaRizeni) !!}';

window.addEventListener("load", function(){
    histogram('el_delkaRizeni', delkaRizeni_json);
});
</script>

@endsection
