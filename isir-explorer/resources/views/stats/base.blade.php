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

                <div class="card  mt-4">
                    <div class="card-header">
                        <h1>{{ $nazevStatistiky }}</h1>
                    </div>
                    <div class="card-header">
                        <form method="GET">
                            @include('components.formularFilteru')
                        </form>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-12">
                                @yield('graf')
                            </div>
                        </div>
                    </div>

                    @include('components.poznamkyGrafu')
                </div>

            </div>
        </div>
    </div>

@endsection
