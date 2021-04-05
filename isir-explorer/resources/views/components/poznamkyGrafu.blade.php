<div class="card-header">
</div>
<div class="card-body">
    @isset($obdobi)
        @if(!empty($nazevVolbyObdobi))
            Zobrazeny jsou hodnoty pro insolvenční řízení, pro která je {{ mb_strtolower($nazevVolbyObdobi) }}
        @else
            Zobrazeny jsou hodnoty pro insolvenční řízení zahájena v období
        @endif
        mezi {{ $obdobi->od->format("j. n. Y") }} a {{ $obdobi->do->format("j. n. Y") }}.
    @endisset

    @foreach ($poznamky as $pozn)
        <br>{!!$pozn!!}
    @endforeach
</div>
