@extends('layouts.app')

@section('header')
    <script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
        integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
        crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
        integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
        crossorigin=""></script>

    <script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>

    <script defer src="{{ asset('js/maps.js') }}"></script>
    <script defer src="{{ asset('js/detail-veritel.js') }}"></script>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

    <style>



    </style>
@endsection

@section('title')
 | {{ $veritel->nazev }} - detail věřitele
@endsection

@section('content')

    <div class="container">
        <div class="row">
            <div class="col-md-12">

                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{ route("veritele.ins") }}">Věřitelé</a></li>
                    <li class="breadcrumb-item active"">{{ $veritel->nazev }}</li>
                </ol>

                <div class="card">
                    <div class="card-header subject_header">
                        <h1>{{ $veritel->nazev }}</h1>
                        @if(!empty($veritel->ic))
                            <div class="subject_ic">
                                IČ: <a href="https://or.justice.cz/ias/ui/rejstrik-$firma?ico={{ $veritel->ic }}" target="_blank">{{ $veritel->ic }}</a>
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4 veritel-info">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h2>Informace o věřiteli</h2>
                        <table class="table table-hover mt-4 key-value">
                            <tbody>
                                <tr>
                                    <th scope="row">Insolvencí celkem</th>
                                    <td>{{ $veritel->ins_celkem ?? 0 }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Počet pohledávek</th>
                                    <td>{{ $veritel->ins_celkem ?? "nezjištěn" }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Celková výše</th>
                                    <td>{{ formatKc($veritel->vyse_celkem ?? 0) }} Kč</td>
                                </tr>
                                <tr>
                                    <th scope="row">Výše nezajištěných</th>
                                    <td>{{ formatKc($veritel->vyse_nezaj ?? 0) }} Kč</td>
                                </tr>
                                <tr>
                                    <th scope="row">Výše zajištěných</th>
                                    <td>{{ formatKc($veritel->vyse_zaj ?? 0) }} Kč</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card mt-4">
                    <div class="card-body">
                        <h2>Míra přečtení dat</h2>
                        <table class="table table-hover mt-4 key-value">
                            <tr>
                                <th scope="row">Přihláška pohledávky</th>
                                <td>{{ $mira_precteni['pp'] }} / {{ $mira_precteni['celkem'] }}</td>
                            </tr>
                            <tr>
                                <th scope="row">Celkem</th>
                                <td>{{ formatKc($mira_precteni['mira']) }} %</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h2>Ins. řízení dle krajů</h2>

                        <script>
                            var mapData = '{!! json_encode($kraje) !!}';
                            var mapboxToken = '{{ config('app.mapbox_key') }}';
                            var infobox_metric = 'Počet insolvencí';
                            var typyRizeni = '{!! json_encode($ins_stats) !!}';
                        </script>
                        <div class="mt-4" id="map"></div>

                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h2>Typy řízení</h2>
                        @if ($ins_stats)
                            <div class="mt-4" id="typy_chart"></div>
                        @else
                            Údaje nejsou k dispozici.
                        @endif
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h2>Velikosti insolvencí</h2>
                        @if ($ins_stats)
                            <div class="mt-4" id="velikosti_chart"></div>
                        @else
                            Údaje nejsou k dispozici.
                        @endif
                    </div>
                </div>
            </div>
        </div>

    </div>


@endsection
