@extends('layouts.app')

@section('header')
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
crossorigin=""></script>

<script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>

<script defer src="{{ asset('js/maps.js') }}" ></script>

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

<style>

    #map{
        width: 100%;
        min-height: 500px;
    }

    .info {
        padding: 6px 8px;
        font: 14px/16px Arial, Helvetica, sans-serif;
        background: white;
        background: rgba(255,255,255,0.8);
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
        border-radius: 5px;
    }

    .table th, .table td {
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
                        <div class="row">
                            <div class="col-md-8">
                                <h1>{{ $nazevMapy }}</h1>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <select class="date-changer custom-select">
                                        @foreach ($varianty as $v)
                                            <option value="{{$v->id}}" data-rok="{{$v->rok}}" data-mesic="{{$v->mesic}}" @if($v->id == $datarow->id)selected=""@endif>
                                                @if($v->rok != null)
                                                    {{$v->rok}}@if($v->mesic != null)/{{sprintf('%02d', $v->mesic)}}@endif
                                                @else
                                                    Celkem
                                                @endif
                                            </option>
                                        @endforeach
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-8">
                                <script>
                                    var mapData='{!! json_encode($data) !!}';
                                    var mapboxToken='{{ config('app.mapbox_key') }}';
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

                </div>
            </div>
        </div>
    </div>

@endsection
