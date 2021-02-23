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
                        <h1>{{ $nazevMapy }}</h1>
                    </div>
                    <div class="card-header">
                        <form method="GET">
                            <div class="form-group row">
                                <label for="insObdobi" class="col-sm-2 col-form-label">Období zahájení řízení</label>
                                <div class="col-sm-10">
                                    <select name="obdobi" class="form-control" id="insObdobi">
                                        @foreach ($varianty as $v)
                                            <option @if($v == Request::get('obdobi'))selected=""@endif>{{ $v }}</option>
                                        @endforeach
                                    </select>
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="insDluznik" class="col-sm-2 col-form-label">Dlužník</label>
                                <div class="col-sm-10">
                                    @php
                                        $typOsoby = [
                                            ["", "Všechny typy"],
                                            ["FN", "Fyzická osoba - nepodnikatel"],
                                            ["FP", "Fyzická osoba - podnikatel"],
                                            ["P", "Právnická osoba"],
                                        ];
                                    @endphp
                                    <select name="typOsoby" class="form-control" id="insDluznik">
                                        @foreach ($typOsoby as $item)
                                            <option value="{{$item[0]}}" {{ Request::get('typOsoby') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
                                        @endforeach
                                    </select>
                                </div>
                            </div>
                            <div class="form-group row">
                                <label for="insZpusob" class="col-sm-2 col-form-label">Způsob řešení</label>
                                <div class="col-sm-10">
                                    @php
                                        $insZpusob = [
                                            ["", "Všechny způsoby"],
                                            ["O", "Oddlužení"],
                                            ["K", "Konkurz"],
                                            ["R", "Reorganizace"],
                                        ];
                                    @endphp
                                    <select name="zpusobReseni" class="form-control" id="insZpusob">
                                        @foreach ($insZpusob as $item)
                                            <option value="{{$item[0]}}" {{ Request::get('zpusobReseni') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
                                        @endforeach
                                    </select>
                                </div>
                            </div>
                            <div class="form-group row" style="margin-top: 0.5rem">
                                <div class="col-12 text-right">
                                    <button type="submit" class="btn btn-primary"><i class="fa fa-filter"></i> Filtrovat</button>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-8">
                                <script>
                                    var mapData = '{!!  json_encode($data) !!}';
                                    var mapboxToken = '{{ config('app.mapbox_key') }}';

                                </script>
                                <div id="map"></div>
                            </div>
                            <div class="col-lg-4 mt-4 mt-lg-0">
                                <table class="table table-hover">
                                    <thead>
                                        <tr>
                                            <th>Kraj</th>
                                            <th>{{ $nazevHodnoty }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        @foreach ($data as $key => $value)
                                            <tr>
                                                <td>{{ $nazvyKraju[$key] }}</td>
                                                <td>{{ $value }}</td>
                                            </tr>
                                        @endforeach
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div class="card-header">
                    </div>
                    <div class="card-body">
                        Zobrazena jsou insolvenční řízení zahájena v období mezi {{ $obdobi->od->format("j. n. Y") }} a {{ $obdobi->do->format("j. n. Y") }}.
                    </div>

                </div>
            </div>
        </div>
    </div>

@endsection
