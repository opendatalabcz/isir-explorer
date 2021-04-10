@php($classFormLabels = "col-sm-6 col-lg-5")
@php($classFormFields = "col-sm-6 col-lg-7")

<form method="GET">
    <div class="row">

        @if(in_array('obdobi', $nastaveni))
            <div class="col-lg-6">
                @include('components.filters.obdobi')
            </div>
        @endif

        @if(in_array('typOsoby', $nastaveni))
            <div class="col-lg-6">
                @include('components.filters.typOsoby')
            </div>
        @endif

        @if(in_array('insZpusob', $nastaveni))
            <div class="col-lg-6">
                @include('components.filters.insZpusob')
            </div>
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
    </div>

    @include('components.filters.potvrditFiltr')
</form>
