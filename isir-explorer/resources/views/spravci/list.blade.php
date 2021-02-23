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

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>Název subjektu</th>
                                    <th>IČ</th>
                                    <th>Insolvence</th>
                                    <th>Aktivní</th>
                                    <th>Detail</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($spravci as $spravce)
                                    <tr>
                                        <td>{{ $spravce->nazev }}</td>
                                        <td>{{ $spravce->ic }}</td>
                                        <td>{{ $spravce->ins_celkem }}</td>
                                        <td>{{ $spravce->ins_aktivnich }}</td>
                                        <td><a href="{{ route("spravci.detail", ['id' => $spravce->id]) }}">Detail</a></td>
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
