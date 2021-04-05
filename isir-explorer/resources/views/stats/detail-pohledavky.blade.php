@extends('stats.base')

@section('graf')

<div id="el_pohledavky"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var pohledavky_json = '{!!  json_encode($pohledavky) !!}';

window.addEventListener("load", function(){
    histogram('el_pohledavky', pohledavky_json);
});
</script>

@endsection
