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

    <script defer src="{{ mix('js/maps.js') }}"></script>
    <script defer src="{{ mix('js/detail-spravce.js') }}"></script>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

    <style>



    </style>
@endsection

@section('title')
 | {{ $spravce->nazev }} - detail správce
@endsection

@section('content')

    <div class="container">
        <div class="row">
            <div class="col-md-12">

                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{ route("spravci.ins") }}">Správci</a></li>
                    <li class="breadcrumb-item active"">{{ $spravce->nazev }}</li>
                </ol>

                <div class="card">
                    <div class="card-header subject_header">
                        <h1>{{ $spravce->nazev }}</h1>
                        @if(!empty($spravce->ic))
                            <div class="subject_ic">
                                IČ: <a href="https://or.justice.cz/ias/ui/rejstrik-$firma?ico={{ $spravce->ic }}" target="_blank">{{ $spravce->ic }}</a>
                            </div>
                        @endif
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4 spravce-info">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h2>Informace o správci</h2>
                        <table class="table table-hover mt-4 key-value">
                            <tbody>
                                <tr>
                                    <th scope="row">Aktivních insolvencí</th>
                                    <td>{{ $spravce->ins_aktivnich }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Celkem insolvencí</th>
                                    <td>{{ $spravce->ins_celkem }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">První evidované řízení</th>
                                    <td>{{ $info['zahajeniCinnosti']->translatedFormat('F Y') }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Nejnovější řízení</th>
                                    <td>{{ $spravce?->posledni_ins->translatedFormat('F Y') ?? '-' }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card mt-4">
                    <div class="card-body">
                        <h2>Míra přečtení dat</h2>
                        <table class="table table-hover mt-4 key-value">
                            <tbody>
                                <tr>
                                    <th scope="row">Zpráva pro oddlužení</th>
                                    <td>{{ $mira_precteni['zpro'] }} / {{ $mira_precteni['celkem'] }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Splnění oddlužení</th>
                                    <td>{{ $mira_precteni['zspo'] }} / {{ $mira_precteni['celkem'] }}</td>
                                </tr>
                                <tr>
                                    <th scope="row">Celkem</th>
                                    <td>{{ formatKc($mira_precteni['mira']) }} %</td>
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
                            var mapData = '{!! json_encode($kraje) !!}';
                            var mapboxToken = '{{ config('app.mapbox_key') }}';
                            var infobox_metric = 'Počet insolvencí';
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

        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h2>Velikosti insolvencí dle počtu pohledávek</h2>
                        @if ($ins_stats)
                            <div class="mt-4" id="typy_pohl"></div>
                        @else
                            Údaje nejsou k dispozici.
                        @endif
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h2>Výše popřených pohledávek</h2>
                        @if ($ins_stats)
                            <div class="mt-4" id="typy_popreno"></div>
                        @else
                            Údaje nejsou k dispozici.
                        @endif
                    </div>
                </div>
            </div>

        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body table-card">
                        <h2>Poslední evidované odměny z oddlužení</h2>

                        @if(!empty($odmeny))
                            @include('spravci.partials.tabulka-odmen')
                            <a class="btn btn-primary pull-right" href="{{ route('spravci.detail.odmeny', ['id' => $spravce->id]) }}">Zobrazit vše</a>
                        @else
                            Žádné údaje o odměnách toho správce nejsou k dispozici.
                        @endif
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <h2>Poslední skončená oddlužení</h2>

                        @if(!empty($oddluzeni))

                        <table class="table table-hover mt-4">
                            <thead>
                                <tr>
                                    <th>Ins. řízení</th>
                                    <th>Ukončení</th>
                                    <th>Délka (roky)</th>
                                    <th>Velikost (Kč)</th>
                                    <th>Výsledek</th>
                                    <th>Uspokojeno</th>
                                    <th>Celková odměna (Kč)</th>
                                    <th>Uhrazeno</th>
                                    <th>Zdroj</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($oddluzeni as $odmena)
                                    <tr>
                                        <td><a target="_blank" href="{{getInsLink($odmena->spisovaznacka)}}">{{ $odmena->spisovaznacka }}</a></td>
                                        <td data-text="{{$odmena->zverejneni}}">{{ \Carbon\Carbon::parse($odmena->zverejneni)->format('j. n. Y') }}</td>
                                        <td data-text="{{round($odmena->delka_oddluzeni)}}">{{ formatKc(round($odmena->delka_oddluzeni/365,2)) }}</td>
                                        <td data-text="{{round($odmena->celkova_vyse)}}">{{ formatKc($odmena->celkova_vyse) }}</td>
                                        <td>{{ $odmena->vysledek_oddluzeni ? "Splněno" : "Zrušeno"}}</td>
                                        <td>{{ $odmena->n_uspokojeni_mira ? $odmena->n_uspokojeni_mira . " %" : ""}}</td>
                                        <td data-text="{{round($odmena->celkova_odmena)}}">{{ formatKc($odmena->celkova_odmena) }}</td>
                                        <td data-text="{{round($odmena->uhrazeno)}}">{{ round($odmena->uhrazeno) }} %</td>
                                        <td><a target="_blank" href="{{getInsDocLink($odmena->isir_id)}}">Dokument</a></td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>


                        @else
                            Žádné údaje o odměnách toho správce nejsou k dispozici.
                        @endif
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <h2>Časová osa ins. řízení správce</h2>
                        <div id="spravce-timeline" class="mt-4" style="height: 600px;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        var timeline = '{!!  json_encode($timeline) !!}';
        var typyRizeni = '{!! json_encode($ins_stats) !!}';
    </script>


@endsection
