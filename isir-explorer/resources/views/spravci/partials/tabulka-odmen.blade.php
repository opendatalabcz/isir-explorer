<table class="table table-hover mt-4">
    <thead>
        <tr>
            <th>Ins. řízení</th>
            <th>Zveřejnění</th>
            <th>Délka (roky)</th>
            <th>Celková odměna (Kč)</th>
            <th>Hotové výdaje (Kč)</th>
            <th>Uhrazeno</th>
            <th>Zdroj</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($odmeny as $odmena)
            <tr>
                <td><a target="_blank" href="{{getInsLink($odmena->spisovaznacka)}}">{{ $odmena->spisovaznacka }}</a></td>
                <td data-text="{{$odmena->zverejneni}}">{{ \Carbon\Carbon::parse($odmena->zverejneni)->format('j. n. Y') }}</td>
                <td data-text="{{round($odmena->delka_oddluzeni)}}">{{ formatKc(round($odmena->delka_oddluzeni/365,2)) }}</td>
                <td data-text="{{round($odmena->celkova_odmena)}}">{{ formatKc($odmena->celkova_odmena) }}</td>
                <td data-text="{{round($odmena->hotove_vydaje)}}">{{ formatKc($odmena->hotove_vydaje) }}</td>
                <td>{{ round($odmena->uhrazeno) }} %</td>
                <td><a target="_blank" href="{{getInsDocLink($odmena->isir_id)}}">Dokument</a></td>
            </tr>
        @endforeach
    </tbody>
</table>
