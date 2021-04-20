@extends('stats.base')

@section('graf')

<div id="el_prijmyDluznika"></div>
@include('components.zmenaRozliseniHistogr')

<script>
var prijmyDluznika_json = '{!!  json_encode($prijmyDluznika) !!}';

window.addEventListener("load", function(){
    histogram('el_prijmyDluznika', prijmyDluznika_json);
});
</script>

@endsection
