@extends('layouts.app')

@section('header')

    <script defer src="https://cdn.jsdelivr.net/npm/tablesorter@2.31.3/dist/js/jquery.tablesorter.combined.min.js"></script>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

@endsection

@section('content')

    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h1>Počet nových insolvencí v roce 2019</h1>
                    </div>
                    <div class="card-body">
                        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
                        <div id="chart_div"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <style>
        #chart_div{
            min-height: 400px;
        }
    </style>

    <script>
        var json = '{!!  json_encode($data) !!}';
        var insData = JSON.parse(json);
        var arr = [['Měsíc', 'Ins']];

        for(const m in insData){
            arr.push([m, insData[m]]);
        }

        google.charts.load('current', {
            packages: ['corechart', 'bar']
        });
        google.charts.setOnLoadCallback(drawAnnotations);

        function drawAnnotations() {
            var data = new google.visualization.arrayToDataTable(arr);


            var options = {
                legend: { position: "none" },
                annotations: {
                    alwaysOutside: true,
                    textStyle: {
                        fontSize: 14,
                        color: '#000',
                        auraColor: 'none'
                    }
                },
                vAxis: {
                    title: 'Počet nových ins.'
                }
            };

            var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
            chart.draw(data, options);
        }

    </script>

@endsection
