@extends('layouts.app')

@section('header')

    <script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">
    <script defer src="https://www.gstatic.com/charts/loader.js"></script>
    <script defer src="{{ asset('js/grafy.js') }}"></script>
    <script defer src="https://cdn.plot.ly/plotly-latest.min.js"></script>

@endsection

@section('content')

    <div class="container">

        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h1>Statistiky reorganizací</h1>
                    </div>
                    <div class="card-body">
                        Reorganizace je určena pro řešení úpadku podnikatelů s ročním obratem alespoň 50 000 000 Kč. Vyznačuje se tím, že během ní zůstává podnikatelská činnost dlužníka nepřerušena, je-li tato činnost v mezích reorganizačního plánu. Toto řešení je často pro věřitele výhodné, protože pokud je reorganizace úspěšná, je větší pravděpodobnost, že se jejich pohledávky podaří uspokojit ve větší míře, než při řešení konkursem, kdy by bylo podnikání dlužníka zastaveno.
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet nových reorganizací</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pocetNovychRoky"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.pocet', ['zpusobReseni'=>'R', 'poLetech'=>1]) }}">Detail</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet nových reorganizací v roce 2020</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pocetNovychIns"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.pocet', ['zpusobReseni'=>'R']) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Typ osoby dlužníka</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_typyOsob"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.dluznik.typ', ['zpusobReseni'=>'R']) }}">Detail</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Věk dlužníka</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_vekDluznika"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.dluznik.vek', ['zpusobReseni'=>'R']) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Délka řízení</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_delkaRizeni"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.rizeni.delka', ['zpusobReseni'=>'R', 'obdobi' => 2010]) }}">Detail</a>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet pohledávek</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pohledavky"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.rizeni.pohledavky', ['zpusobReseni'=>'R', 'obdobi' => 2019]) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        var pocetNovychIns_json = '{!!  json_encode($pocetNovychMes) !!}';
        var pocetNovychRoky_json = '{!!  json_encode($pocetNovychRoky) !!}';
        var typyOsob_json = '{!!  json_encode($typOsoby) !!}';
        var vekDluznika_json = '{!!  json_encode($vekDluznika) !!}';
        var delkaRizeni_json = '{!!  json_encode($delkaRizeni) !!}';
        var pohledavky_json = '{!!  json_encode($pohledavky) !!}';

        window.addEventListener("load", function(){
            google.charts.load('current', {
                packages: ['corechart', 'bar']
            });
            google.charts.setOnLoadCallback(drawCharts);

            //plotly calls
            histogram('el_vekDluznika', vekDluznika_json);
            histogram('el_delkaRizeni', delkaRizeni_json);
            histogram('el_pohledavky', pohledavky_json);
        });

        function drawCharts(){
            pocetNovychIns('el_pocetNovychIns', pocetNovychIns_json);
            pocetNovychIns('el_pocetNovychRoky', pocetNovychRoky_json);
            typOsoby('el_typyOsob', typyOsob_json);
        }
    </script>

@endsection
