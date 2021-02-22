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

        .key-value td {
            text-align:right;
        }


    </style>
@endsection

@section('content')

    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h1>{{ $spravce->nazev }}</h1>
                    </div>
                </div>
            </div>
        </div>



        <div class="row mt-4">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h2>Informace o správci</h2>
                        <table class="table table-hover mt-4 key-value">
                            <tbody>
                                <tr>
                                    <th scope="row">Aktivních insolvencí</th>
                                    <td>49</td>
                                </tr>
                                <tr>
                                    <th scope="row">Celkem insolvencí</th>
                                    <td>500</td>
                                </tr>
                                <tr>
                                    <th scope="row">Zahájení činnosti</th>
                                    <td>{{ $info['zahajeniCinnosti']->translatedFormat('F Y') }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h2>Ins. řízení správce dle krajů</h2>

                        <script>
                            var mapData = '{!!  json_encode($kraje) !!}';
                            var mapboxToken = '{{ config('app.mapbox_key') }}';
                        </script>
                        <div class="mt-4" id="map"></div>

                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <h2>Přehled ins. řízení správce</h2>
                        <div id="timeline" class="mt-4" style="height: 600px;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <style>
        .ti-tt {
            min-height: 100px;
            min-width: 300px;
            padding: 1em 1.5em 0 1em;
        }

        .ti-title {
            font-size: 1rem;
            display: block;
            font-weight: bold;
            width: 100%;
            border-bottom: 1px solid grey;
            margin-bottom: 0.5rem;
            padding-bottom: 0.2rem;
        }

        dl.ti-info {
            display: grid;
            grid-template-columns: max-content auto;
            grid-gap: 0 1rem;
        }

        dt {
            grid-column-start: 1;
        }

        dd {
            grid-column-start: 2;
        }

    </style>
    <script>
        var timeline = '{!!  json_encode($timeline) !!}';
        google.charts.load('current', {
            'packages': ['timeline'],
            'language': 'cs',
        });
        google.charts.setOnLoadCallback(drawChart);

        Date.prototype.dmy = function() {
            var m = this.getMonth() + 1;
            var d = this.getDate();

            return d + '. ' + m + '. ' + this.getFullYear();
        };

        function drawChart() {
            var container = document.getElementById('timeline');
            var chart = new google.visualization.Timeline(container);
            var dataTable = new google.visualization.DataTable();

            dataTable.addColumn({
                type: 'string',
                id: 'INS'
            });
            dataTable.addColumn({
                type: 'string',
                id: 'INS'
            });
            dataTable.addColumn({
                type: 'string',
                id: 'style',
                role: 'style'
            });
            dataTable.addColumn({
                type: 'string',
                role: 'tooltip',
            });
            dataTable.addColumn({
                type: 'date',
                id: 'Zacatek'
            });
            dataTable.addColumn({
                type: 'date',
                id: 'Konec'
            });

            timeline = JSON.parse(timeline);
            let rows = [];
            const colors = {
                "O": "#127ba3",
                "K": "#ff7700",
                "R": "#009420",
                "?": "#292929",
            };
            const typNazvy = {
                "O": "Oddlužení",
                "K": "Konkurz",
                "R": "Reorganizace",
                "?": "Neurčeno",
            };

            function typRizeni(ins) {
                let col = colors[ins.t];
                return '<span style="color:' + col + ';font-weight:bol">' + typNazvy[ins.t] + '</span>';
            }

            function tooltipHtml(ins, zacatek, konec) {
                const now = new Date();
                const diffTime = Math.abs(now - konec);
                const ukonceni = (diffTime < 1000 * 60 * 60 * 24) ? "<em>Současnost</em>" : konec.dmy();
                let title = '<span class="ti-title">' + ins.i + '</span>'
                let vlasnosti = '<dl class="ti-info"><dt>Typ:</dt><dd>' + typRizeni(ins) + '</dd>';
                vlasnosti += '<dt>Zahájení:</dt><dd>' + zacatek.dmy() + '</dd>';
                vlasnosti += '<dt>Ukončení:</dt><dd>' + ukonceni + '</dd>';
                vlasnosti += '</dl>';
                return '<div class="ti-tt">' + title + vlasnosti + '</div>';
            }
            for (const ins of timeline) {
                let zacatek = new Date(ins.s * 1000);
                let konec = new Date(ins.e * 1000);
                rows.push([
                    ins.i, "", colors[ins.t], tooltipHtml(ins, zacatek, konec), zacatek, konec,
                ]);
            }

            dataTable.addRows(rows);
            var options = {
                timeline: {
                    showRowLabels: false,
                    barLabelStyle: {
                        fontSize: 3
                    }
                },
                tooltip: {
                    isHtml: true
                },
            };

            chart.draw(dataTable, options);
        }

    </script>


@endsection
