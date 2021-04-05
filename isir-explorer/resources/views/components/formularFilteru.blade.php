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

    @include('components.filters.potvrditFiltr')
</form>
