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
                    <li class="nav-item active">
                        <a class="nav-link" href="#">Insolvence
                            <span class="sr-only">(aktivní)</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Dlužníci</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Věřitelé</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Správci</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button"
                            aria-haspopup="true" aria-expanded="false">Statistiky</a>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="#">Mapy</a>
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
</body>

</html>
