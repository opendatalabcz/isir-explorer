@extends('stats.base')

@section('graf')

<div id="el_vekDluznika"></div>

<div class="row">
    <div class="col-lg-8">
        <label for="resRange">Rozlišení</label>
    </div>
    <div class="col-lg-4" style="text-align: right">
        <span id="resVal">?</span> {{ $jednotkaRozsahu }}
    </div>
</div>
<input type="range" id="resRange">

<script>
var vekDluznika_json = '{!!  json_encode($vekDluznika) !!}';

window.addEventListener("load", function(){
    histogram('el_vekDluznika', vekDluznika_json);
});
</script>

@endsection
