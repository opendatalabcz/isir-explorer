<form method="GET">
    @if(in_array('obdobi', $nastaveni))
        @include('components.filters.obdobi')
    @endif

    @if(in_array('typOsoby', $nastaveni))
        @include('components.filters.typOsoby')
    @endif

    @if(in_array('insZpusob', $nastaveni))
        @include('components.filters.insZpusob')
    @endif

    @if(in_array('poLetech', $extraNastaveni))
        @include('components.filters.zobrazitPoLetech')
    @endif

    @if(in_array('typPohledavky', $extraNastaveni))
        @include('components.filters.typPohledavky')
    @endif

    @if(in_array('idRozsahu', $extraNastaveni))
        @include('components.filters.idRozsahuZobrazeni')
    @endif


    @include('components.filters.potvrditFiltr')
</form>
