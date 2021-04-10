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
                        <h1>Věřitelé</h1>
                    </div>
                    <div class="card-body">
                        <p>Věřitel je osoba, které náleží plnění nějaké pohledávky od osoby dlužníka. Věřitelé do řízení vstupují podáním tzv. přihlášky pohledávky. V tomto přehledovém seznamu je zobrazeno až 1000 věřitelů seřazených dle vybraného parametru. V seznamu nejsou zahrnuty nepodnikající fyzické osoby. Zdrojem počtů insolvencí u jednotlivých věřitelů jsou údaje z insolvenčního rejstříku. Zdrojem údajích o přihláškách a velikostech pohledávek jsou čteny z dokumentů přihlášek a údaje tak nemusí být kompletní ze všech pohledávek, které věřitel přihlásil.</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="card mt-4">
            <div class="card-header">
                <h3>Typ zobrazení</h3>
            </div>
            <div class="card-header">
                @foreach (\App\Http\Controllers\VeriteleController::TYP_ZOBRAZENI as $routeId => $info)
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
                                    @elseif($zobrazeni == 'vyse-pohledavek')
                                        <th class="text-right">Celková&nbsp;výše&nbsp;(Kč)</th>
                                        <th class="text-right">Výše&nbsp;nezajištěných&nbsp;(Kč)</th>
                                        <th class="text-right">Výše&nbsp;zajištěných&nbsp;(Kč)</th>
                                    @elseif($zobrazeni == 'vyse-zaj-pohledavek')
                                        <th class="text-right">Celková&nbsp;výše&nbsp;(Kč)</th>
                                        <th class="text-right">Výše&nbsp;zajištěných&nbsp;(Kč)</th>
                                    @elseif($zobrazeni == 'prumerna-vyse-pohledavky')
                                        <th class="text-right">Počet&nbsp;přihlášek</th>
                                        <th class="text-right">Průměrná&nbsp;výše<br>v&nbsp;přihlášce&nbsp;(Kč)</th>
                                    @elseif($zobrazeni == 'pohledavek-v-prihlasce')
                                        <th class="text-right">Počet&nbsp;přihlášek</th>
                                        <th class="text-right">Počet&nbsp;pohledávek</th>
                                        <th class="text-right">Průměrný počet pohl.<br>v&nbsp;přihlášce&nbsp;</th>
                                    @endif

                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($veritele as $veritel)
                                    <tr>
                                        <td>
                                            <a href="{{ route("veritele.detail", ['id' => $veritel->id]) }}">{{ $veritel->nazev }}</a>
                                        </td>

                                        @if($zobrazeni == 'pocty-insolvenci')
                                        <td class="text-right">
                                            @isset($veritel->ic)
                                                <a href="https://or.justice.cz/ias/ui/rejstrik-$firma?ico={{ $veritel->ic }}" target="_blank">{{ $veritel->ic }}</a>
                                            @else
                                                -
                                            @endisset
                                        </td>
                                        @endif

                                        @if($zobrazeni == 'pocty-insolvenci')
                                            <td class="text-right">{{ $veritel->ins_celkem }}</td>
                                        @elseif($zobrazeni == 'vyse-pohledavek')
                                            <td class="text-right"
                                                data-text="{{round($veritel->vyse_celkem)}}">
                                                {{ formatKc($veritel->vyse_celkem) }}</td>
                                            <td class="text-right"
                                                data-text="{{round($veritel->vyse_nezaj)}}">
                                                {{ formatKc($veritel->vyse_nezaj) }}</td>
                                            <td class="text-right"
                                                data-text="{{round($veritel->vyse_zaj)}}">
                                                {{ formatKc($veritel->vyse_zaj) }}</td>
                                        @elseif($zobrazeni == 'vyse-zaj-pohledavek')
                                            <td class="text-right"
                                                data-text="{{round($veritel->vyse_celkem)}}">
                                                {{ formatKc($veritel->vyse_celkem) }}</td>
                                            <td class="text-right"
                                                data-text="{{round($veritel->vyse_zaj)}}">
                                                {{ formatKc($veritel->vyse_zaj) }}</td>
                                        @elseif($zobrazeni == 'prumerna-vyse-pohledavky')
                                            <td class="text-right">{{ $veritel->prihlasky_pocet }}</td>
                                            <td class="text-right"
                                                data-text="{{round($veritel->vyse_celkem/$veritel->prihlasky_pocet)}}">
                                                {{ formatKc($veritel->vyse_celkem/$veritel->prihlasky_pocet) }}</td>
                                        @elseif($zobrazeni == 'pohledavek-v-prihlasce')
                                            <td class="text-right">{{ $veritel->prihlasky_pocet }}</td>
                                            <td class="text-right">{{ $veritel->pohledavky_pocet }}</td>
                                            <td class="text-right"
                                                data-text="{{round($veritel->pohledavky_pocet/$veritel->prihlasky_pocet)}}">
                                                {{ formatKc($veritel->pohledavky_pocet/$veritel->prihlasky_pocet) }}</td>
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
});
};
</script>
@endsection
