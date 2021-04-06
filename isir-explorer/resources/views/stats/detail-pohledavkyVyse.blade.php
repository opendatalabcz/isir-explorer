@extends('stats.base')

@section('graf')

<div id="el_pohledavkyVyse"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var pohledavky_json = '{!!  json_encode($pohledavkyVyse) !!}';

window.addEventListener("load", function(){
    histogram('el_pohledavkyVyse', pohledavky_json);
});
</script>

@endsection
