@extends('layouts.app')

@section('header')
<script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

@endsection

@section('title')
 | {{ $spravce->nazev }} - odměny správce
@endsection

@section('content')

    <div class="container">
        <div class="row">
            <div class="col-md-12">

                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{ route("spravci.ins") }}">Správci</a></li>
                    <li class="breadcrumb-item"><a href="{{ route("spravci.detail", ['id' => $spravce->id]) }}">{{ $spravce->nazev }}</a></li>
                    <li class="breadcrumb-item active">Odměny</li>
                </ol>

                <div class="card">
                    <div class="card-header">
                        <h1>Odměny správce {{ $spravce->nazev }}</h1>
                    </div>
                    <div class="card-body">
                        @include('spravci.partials.tabulka-odmen')
                    </div>

                </div>
            </div>
        </div>

    </div>

<script>
window.onload = function(){
$("table").tablesorter({
    theme : "bootstrap",
    widthFixed: true,
    widgets : ["columns"],
});
};
</script>
@endsection
