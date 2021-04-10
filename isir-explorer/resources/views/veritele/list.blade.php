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
                        <p>TODO</p>
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

                                    @if($zobrazeni != 'velikosti-insolvenci')
                                        <th class="text-right">IČ</th>
                                    @endif

                                    @if($zobrazeni == 'pocty-insolvenci')
                                        <th class="text-right">Insolvence</th>
                                        <th class="text-right">Aktivní</th>
                                    @endif
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($spravci as $spravce)
                                    <tr>
                                        <td>
                                            <a href="{{ route("spravci.detail", ['id' => $spravce->id]) }}">{{ $spravce->nazev }}</a>
                                        </td>

                                        @if($zobrazeni != 'velikosti-insolvenci')
                                        <td class="text-right">
                                            @isset($spravce->ic)
                                                <a href="https://or.justice.cz/ias/ui/rejstrik-$firma?ico={{ $spravce->ic }}" target="_blank">{{ $spravce->ic }}</a>
                                            @else
                                                -
                                            @endisset
                                        </td>
                                        @endif

                                        @if($zobrazeni == 'pocty-insolvenci')
                                            <td class="text-right">x</td>
                                            <td class="text-right">x</td>
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
