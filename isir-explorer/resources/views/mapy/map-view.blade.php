@extends('layouts.app')

@section('header')
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
        integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
        crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
        integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
        crossorigin=""></script>

    <script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>

    <script defer src="{{ asset('js/maps.js') }}"></script>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

    <style>
        #map {
            width: 100%;
            min-height: 500px;
        }

        .info {
            padding: 6px 8px;
            font: 14px/16px Arial, Helvetica, sans-serif;
            background: white;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            border-radius: 5px;
        }

        .table th,
        .table td {
            padding: 0.374rem !important;
        }

    </style>
@endsection

@section('content')

    <div class="container">
        <div class="row">
            <div class="col-md-12">

                <div class="card">
                    <div class="card-header">
                        <h3>Statistiky krajů</h3>
                    </div>
                    <div class="card-header">
                        @foreach (\App\Http\Controllers\Maps\MapIndex::MAPY as $routeId => $mapInfo)
                            @if(\Request::route()->getName() == $routeId)
                                <span class="btn btn-link disabled">{{ $mapInfo['nazev'] }}</span>
                            @else
                                <a class="btn btn-link" href="{{ route($routeId) }}">{{ $mapInfo['nazev'] }}</a>
                            @endif

                        @endforeach
                    </div>
                </div>

                <div class="card  mt-4">
                    <div class="card-header">
                        <h1>{{ $nazevMapy }}</h1>
                    </div>
                    <div class="card-header">
                        @include('components.formularFilteru')
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-8">
                                <script>
                                    var mapData = '{!!  json_encode($data) !!}';
                                    var mapboxToken = '{{ config('app.mapbox_key') }}';
                                    var mapInvert = {{$inverze ? "true" : "false" }};
                                    var infobox_metric = '{!!  $nazevHodnotyInfobox !!}';
                                </script>
                                <div id="map"></div>
                            </div>
                            <div class="col-lg-4 mt-4 mt-lg-0">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Kraj</th>
                                            <th>{!! $nazevHodnoty !!}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        @foreach ($data as $key => $value)
                                            <tr>
                                                <td>{{ $nazvyKraju[$key] }}</td>

                                                @if(!$jeCastka)
                                                    <td>{{ $value }}</td>
                                                @else
                                                    <td data-text="{{$value}}">
                                                        {{ formatKc($value) }}
                                                    </td>
                                                @endif

                                            </tr>
                                        @endforeach
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    @include('components.poznamkyGrafu')
                </div>

            </div>
        </div>
    </div>

@endsection
