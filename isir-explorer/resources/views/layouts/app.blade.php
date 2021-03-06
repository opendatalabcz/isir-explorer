<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>{{ config('app.name') }}@yield('title', '')</title>

    <!-- Scripts -->
    <script src="{{ mix('js/app.js') }}" defer></script>

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-SWH8D1FRZY"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-SWH8D1FRZY');
    </script>

    <!-- Styles -->
    <link href="{{ mix('css/app.css') }}" rel="stylesheet">

    <link href="/favicon.ico" rel="shortcut icon" type="image/x-icon" />

    @yield('header')
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">{{ config('app.name') }}</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01"
                aria-controls="navbarColor01" aria-expanded="false" aria-label="Nabídka">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarColor01">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item {{ \str_starts_with(\Request::route()->getName(), "veritele") ? 'active' : '' }}">
                        <a class="nav-link" href="{{ route("veritele.ins") }}">Věřitelé</a>
                    </li>
                    <li class="nav-item {{ \str_starts_with(\Request::route()->getName(), "spravci") ? 'active' : '' }}">
                        <a class="nav-link" href="{{ route("spravci.ins") }}">Správci</a>
                    </li>
                    <li class="nav-item {{ \str_starts_with(\Request::route()->getName(), "stat.mapy") ? 'active' : '' }}">
                        <a class="nav-link" href="{{ route("stat.mapy.ins") }}">Mapy</a>
                    </li>
                    <li class="nav-item dropdown {{
                        \str_starts_with(\Request::route()->getName(), "stat") &&
                        !\str_starts_with(\Request::route()->getName(), "stat.mapy") ? 'active' : '' }}">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button"
                            aria-haspopup="true" aria-expanded="false">Statistiky</a>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="{{ route("stat.prehled.ins") }}">Všechny insolvence</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="{{ route("stat.prehled.oddluzeni") }}">Oddlužení</a>
                            <a class="dropdown-item" href="{{ route("stat.prehled.konkurz") }}">Konkurz</a>
                            <a class="dropdown-item" href="{{ route("stat.prehled.reorg") }}">Reorganizace</a>
                        </div>
                    </li>
                </ul>
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
                <br>
                Kontaktujte nás na: <a href="mailto:info@opendatalab.cz">info@opendatalab.cz</a>
                <br><br>
                <p style="text-align: justify; color: #888;">
                Zdrojem pro data prezentovaná ve statistikách v tomto nástroji je databáze insolvenčního rejstříku a dokumenty v něm zveřejňované.
                Část statistik vychází pouze z dat u takových řízení, kde bylo možné data automatizovaně získat. Správnost takto přečtených údajů z insolvenčních dokumentů není manuálně kontrolována, a v údajích se tak mohou vyskytovat nepřestnosti.
                Provozovatel žádným způsobem neodpovídá za správnost údajů a statistik prezentovaných v nástroji IsirExplorer.
                </p>
            </div>
        </div>
    </footer>
</body>

</html>
