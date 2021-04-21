@extends('layouts.app')

@section('header')

    <script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">
    <script defer src="https://www.gstatic.com/charts/loader.js"></script>
    <script defer src="{{ asset('js/grafy.js') }}"></script>
    <script defer src="https://cdn.plot.ly/plotly-latest.min.js"></script>

@endsection

@section('title')
 | Statistiky konkurzů
@endsection

@section('content')

    <div class="container">

        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h1>Statistiky konkurzů</h1>
                    </div>
                    <div class="card-body">
                        Podstatou konkursu je poměrné uspokojení zjištěných pohledávek věřitelů z výnosu zpeněžení majetku dlužníka. Neuspokojené části pohledávek nebo jejich části po skončení řízení nezanikají. Okamžikem vyhlášení konkursu připadá právo nakládat s majetkem dlužníka na insolvenčního správce. Majetek se zpeněžuje např. prodejem movitých věcí a nemovitostí nebo veřejnou dražbou.
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet nových konkurzů</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pocetNovychRoky"></div>
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.pocet', ['zpusobReseni'=>'K', 'poLetech'=>1]) }}">Detail</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet nových konkurzů v roce 2020</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pocetNovychIns"></div>
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.pocet', ['zpusobReseni'=>'K']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.dluznik.typ', ['zpusobReseni'=>'K']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.dluznik.vek', ['zpusobReseni'=>'K']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.rizeni.delka', ['zpusobReseni'=>'K']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.rizeni.pohledavky', ['zpusobReseni'=>'K']) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Velikosti konkurzů</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pohledavkyVyseCelkem"></div>
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.rizeni.pohledavky.vyse', ['zpusobReseni'=>'K']) }}">Detail</a>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Zajištěné pohledávky</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pohledavkyVyseZaji"></div>
                        <a class="btn btn-info pull-right"
                        href="{{ route('stat.detail.rizeni.pohledavky.vyse', ['zpusobReseni'=>'K', 'typPohledavky' => 'Z']) }}">Detail</a>
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
        var pohledavkyVyseCelkem_json = '{!!  json_encode($pohledavkyVyseCelkem) !!}';
        var pohledavkyVyseZaji_json = '{!!  json_encode($pohledavkyVyseZaji) !!}';

        window.addEventListener("load", function(){
            google.charts.load('current', {
                packages: ['corechart', 'bar'],
                'language': 'cs',
            });
            google.charts.setOnLoadCallback(drawCharts);

            //plotly calls
            histogram('el_vekDluznika', vekDluznika_json);
            histogram('el_delkaRizeni', delkaRizeni_json);
            histogram('el_pohledavky', pohledavky_json);
            histogram('el_pohledavkyVyseCelkem', pohledavkyVyseCelkem_json);
            histogram('el_pohledavkyVyseZaji', pohledavkyVyseZaji_json);
        });

        function drawCharts(){
            pocetNovychIns('el_pocetNovychIns', pocetNovychIns_json);
            pocetNovychIns('el_pocetNovychRoky', pocetNovychRoky_json);
            typOsoby('el_typyOsob', typyOsob_json);
        }
    </script>

@endsection
