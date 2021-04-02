<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">

    <title>{{ config('app.name') }}</title>

    <!-- Scripts -->
    <script src="{{ asset('js/app.js') }}" defer></script>

    <!-- Styles -->
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">

    @yield('header')
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="#">{{ config('app.name') }}</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01"
                aria-controls="navbarColor01" aria-expanded="false" aria-label="Zobrazení menu">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarColor01">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/insolvence">Insolvence</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Dlužníci</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Věřitelé</a>
                    </li>
                    <li class="nav-item {{ \str_starts_with(\Request::route()->getName(), "spravci") ? 'active' : '' }}">
                        <a class="nav-link" href="{{ route("spravci") }}">Správci</a>
                    </li>
                    <li class="nav-item dropdown {{ \str_starts_with(\Request::route()->getName(), "stat") ? 'active' : '' }}">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button"
                            aria-haspopup="true" aria-expanded="false">Statistiky</a>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="{{ route("stat.mapy.ins") }}">Mapy</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Oddlužení</a>
                            <a class="dropdown-item" href="#">Konkurz</a>
                            <a class="dropdown-item" href="#">Reorganizace</a>
                        </div>
                    </li>
                </ul>
                <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="text" placeholder="Hledat">
                    <button class="btn btn-secondary my-2 my-sm-0" type="submit">Hledat</button>
                </form>
            </div>
        </div>
    </nav>

    @yield('content')

    <footer class="container">
        <div class="row">
            <div class="col-md-12">
                &copy; 2021 IsirExplorer
                <br>
                <a href="https://github.com/opendatalabcz/isir-explorer" target="_blank">Zdrojový kod</a> je dostupný pod licencí GNU General Public License v3.0
                <br><br>
                <p style="text-align: justify">
                Zdrojem pro data prezentovaná ve statistikách v tomto nástroji je databáze insolvenčního rejstříku a dokumenty v něm zveřejňované.
                Část statistik vychází pouze z dat u takových řízení, kde bylo možné data automatizovaně získat. Správnost takto přečtených údajů z insolvenčních dokumentů není manuálně kontrolována, a v údajích se tak mohou vyskytovat nepřestnosti.
                Provozovatel žádným způsobem neodpovídá za správnost údajů a statistik prezentovaných v nástroji IsirExplorer.
                </p>
            </div>
        </div>
    </footer>
</body>

</html>
