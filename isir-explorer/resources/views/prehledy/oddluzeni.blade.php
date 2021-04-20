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
                        <h1>Statistiky oddlužení</h1>
                    </div>
                    <div class="card-body">
                        Oddlužení je způsob řešení úpadku fyzických osob, jejichž dluhy nepocházejí z podnikání, nebo právnických osob, které nejsou považovány za podnikatele. Oddlužení se vyznačuje tím, že po jeho splnění dlužníkovy závazky vůči věřitelům zanikají a to i v případě, že se je nepodařilo uspokojit v plné míře. Nesmí však jít o plnění nižší než 30% z celkového dluhu dlužníka.
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet nových oddlužení</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pocetNovychRoky"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.pocet', ['zpusobReseni'=>'O', 'poLetech'=>1]) }}">Detail</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Počet nových oddlužení v roce 2020</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pocetNovychIns"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.pocet', ['zpusobReseni'=>'O']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.dluznik.typ', ['zpusobReseni'=>'O']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.dluznik.vek', ['zpusobReseni'=>'O']) }}">Detail</a>
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
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.rizeni.delka', ['zpusobReseni'=>'O', 'obdobi' => 2010]) }}">Detail</a>
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
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.rizeni.pohledavky', ['zpusobReseni'=>'O', 'obdobi' => 2019]) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Velikosti oddlužení</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_pohledavkyVyseCelkem"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.rizeni.pohledavky.vyse', ['zpusobReseni'=>'O', 'obdobi' => 2019]) }}">Detail</a>
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
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.rizeni.pohledavky.vyse', ['zpusobReseni'=>'O', 'obdobi' => 2019, 'typPohledavky' => 'Z']) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Skutečná míra uspokojení věřitelů</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_miraUspokojeni"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.oddl.mira_uspokojeni', ['miraUspokojeni'=>0, 'zobrazeniTyp' => 'lin']) }}">Detail</a>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Rozdíl míry a předpokladu uspokojení</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_miraUspokojeniRozdil"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.oddl.mira_uspokojeni', ['miraUspokojeni'=>2, 'zobrazeniTyp' => 'log']) }}">Detail</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Příjmy dlužníka</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_prijmyDluznika"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.oddl.prijmy_dluznika', []) }}">Detail</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2>Majetek dlužníka</h2>
                    </div>
                    <div class="card-body">
                        <div class="chartBox sm" id="el_majetekDluznika"></div>
                        <a class="btn btn-info pull-right" href="{{ route('stat.detail.oddl.majetek_dluznika', []) }}">Detail</a>
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
        var miraUspokojeni_json = '{!!  json_encode($miraUspokojeni) !!}';
        var miraUspokojeniRozdil_json = '{!!  json_encode($miraUspokojeniRozdil) !!}';
        var prijmyDluznika_json = '{!!  json_encode($prijmyDluznika) !!}';
        var majetekDluznika_json = '{!!  json_encode($majetekDluznika) !!}';

        window.addEventListener("load", function(){
            google.charts.load('current', {
                packages: ['corechart', 'bar']
            });
            google.charts.setOnLoadCallback(drawCharts);

            //plotly calls
            histogram('el_vekDluznika', vekDluznika_json);
            histogram('el_delkaRizeni', delkaRizeni_json);
            histogram('el_pohledavky', pohledavky_json);
            histogram('el_pohledavkyVyseCelkem', pohledavkyVyseCelkem_json);
            histogram('el_pohledavkyVyseZaji', pohledavkyVyseZaji_json);
            histogram('el_miraUspokojeni', miraUspokojeni_json);
            histogram('el_miraUspokojeniRozdil', miraUspokojeniRozdil_json);
            histogram('el_prijmyDluznika', prijmyDluznika_json);
            histogram('el_majetekDluznika', majetekDluznika_json);
        });

        function drawCharts(){
            pocetNovychIns('el_pocetNovychIns', pocetNovychIns_json);
            pocetNovychIns('el_pocetNovychRoky', pocetNovychRoky_json);
            typOsoby('el_typyOsob', typyOsob_json);
        }
    </script>

@endsection
