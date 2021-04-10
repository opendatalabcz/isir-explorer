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
                        <h1>Insolvenční správci</h1>
                    </div>
                    <div class="card-body">
                        <p>Insolvenční správce je fyzická nebo právnická osoba, kterou lze považovat za administrátora celého insolvenčního řízení. Činnosti mu ukládá insolvenční zákon a zákon o insolvenčních správcích. Mezi jeho úlohy patří například sepsání majetku dlužníka, přezkoumání přihlášených pohledávek nebo uspokojování věřitelů z prostředků dlužníka. Insolvenční správce musí mít pro výkon své činnosti povolení od Ministerstva spravedlnosti, které získá po složení zkoušky insolvenčního správce a splnění dalších zákonem definovaných požadavků. Insolvenčního správce pro konkrétní insolvenční řízení ustanovuje insolvenční soud výběrem ze seznamu insolvenčních správců.</p>
                    </div>

                </div>
            </div>
        </div>

        <div class="card mt-4">
            <div class="card-header">
                <h3>Typ zobrazení</h3>
            </div>
            <div class="card-header">
                @foreach (\App\Http\Controllers\SpravciController::TYP_ZOBRAZENI as $routeId => $info)
                    @if($zobrazeni == $routeId)
                        <span class="btn btn-link disabled">{{ $info['nazev'] }}</span>
                    @else
                        <a class="btn btn-link" href="{{ setUriParam(['zobrazeni' => $routeId]) }}">{{ $info['nazev'] }}</a>
                    @endif

                @endforeach
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Název subjektu</th>

                                    @if($zobrazeni == 'pocty-insolvenci')
                                        <th class="text-right">IČ</th>
                                    @endif

                                    @if($zobrazeni == 'pocty-insolvenci')
                                        <th class="text-right">Insolvence</th>
                                        <th class="text-right">Aktivní</th>
                                    @elseif($zobrazeni == 'velikosti-insolvenci')
                                        <th class="text-right">Počet pohledávek</th>
                                        <th class="text-right">Výše přihlášených<br>pohledávek (Kč)</th>
                                        <th class="text-right">Průměrná výše<br>pohledávky (Kč)</th>
                                    @elseif($zobrazeni == 'evidovana-odmena')
                                        <th class="text-right">Insolvencí</th>
                                        <th class="text-right">Odměna (Kč)</th>
                                        <th class="text-right">Hotové výdaje (Kč)</th>
                                    @elseif($zobrazeni == 'prumerna-odmena')
                                        <th class="text-right">Insolvencí</th>
                                        <th class="text-right">Odměna (Kč)</th>
                                        <th class="text-right">Hotové výdaje (Kč)</th>
                                    @endif
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($spravci as $spravce)
                                    <tr>
                                        <td>
                                            <a href="{{ route("spravci.detail", ['id' => $spravce->id]) }}">{{ $spravce->nazev }}</a>
                                        </td>

                                        @if($zobrazeni == 'pocty-insolvenci')
                                        <td class="text-right">
                                            @isset($spravce->ic)
                                                <a href="https://or.justice.cz/ias/ui/rejstrik-$firma?ico={{ $spravce->ic }}" target="_blank">{{ $spravce->ic }}</a>
                                            @else
                                                -
                                            @endisset
                                        </td>
                                        @endif

                                        @if($zobrazeni == 'pocty-insolvenci')
                                            <td class="text-right">{{ $spravce->ins_celkem }}</td>
                                            <td class="text-right">{{ $spravce->ins_aktivnich }}</td>
                                        @elseif($zobrazeni == 'velikosti-insolvenci')
                                            <td class="text-right">{{ $spravce->agreagace->pohledavky_pocet }}</td>
                                            <td class="text-right"
                                                data-text="{{$spravce->agreagace->celkova_vyse}}">
                                                {{ formatKc($spravce->agreagace->celkova_vyse) }}</td>
                                            <td class="text-right"
                                                data-text="{{round($spravce->agreagace->celkova_vyse / $spravce->agreagace->pohledavky_pocet)}}">
                                                {{ formatKc($spravce->agreagace->celkova_vyse / $spravce->agreagace->pohledavky_pocet) }}</td>
                                        @elseif($zobrazeni == 'evidovana-odmena')
                                            <td class="text-right">{{ $spravce->agreagace->pocet }}</td>
                                            <td class="text-right"
                                                data-text="{{round($spravce->agreagace->celkova_odmena)}}">
                                                {{ formatKc($spravce->agreagace->celkova_odmena) }}</td>
                                            <td class="text-right"
                                                data-text="{{round($spravce->agreagace->hotove_vydaje)}}">
                                                {{ formatKc($spravce->agreagace->hotove_vydaje) }}</td>
                                        @elseif($zobrazeni == 'prumerna-odmena')
                                            <td class="text-right">{{ $spravce->agreagace->pocet }}</td>
                                            <td class="text-right"
                                                data-text="{{round($spravce->agreagace->celkova_odmena)}}">
                                                {{ formatKc($spravce->agreagace->celkova_odmena) }}</td>
                                            <td class="text-right"
                                                data-text="{{round($spravce->agreagace->hotove_vydaje)}}">
                                                {{ formatKc($spravce->agreagace->hotove_vydaje) }}</td>
                                        @endif
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>

                </div>
            </div>
        </div>
    </div>

<script>
window.onload = function(){
$("table").tablesorter({
    theme : "bootstrap",
    widthFixed: true,
    widgets : ["columns"],
    sortList: [[0,0]]
});
};
</script>
@endsection
