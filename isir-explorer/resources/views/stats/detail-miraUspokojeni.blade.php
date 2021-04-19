@extends('stats.base')

@section('graf')

<div id="el_miraUspokojeni"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var miraUspokojeni_json = '{!!  json_encode($miraUspokojeni) !!}';

window.addEventListener("load", function(){
    histogram('el_miraUspokojeni', miraUspokojeni_json);
});
</script>

@endsection
