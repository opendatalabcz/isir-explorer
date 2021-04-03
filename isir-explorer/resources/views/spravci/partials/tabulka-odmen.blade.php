<table class="table table-hover mt-4">
    <thead>
        <tr>
            <th>Ins. řízení</th>
            <th>Zveřejnění</th>
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
                <td>{{ \Carbon\Carbon::parse($odmena->zverejneni)->format('j. n. Y') }}</td>
                <td>{{ formatKc($odmena->celkova_odmena) }}</td>
                <td>{{ formatKc($odmena->hotove_vydaje) }}</td>
                <td>{{ round($odmena->uhrazeno) }} %</td>
                <td><a target="_blank" href="{{getInsDocLink($odmena->isir_id)}}">Dokument</a></td>
            </tr>
        @endforeach
    </tbody>
</table>
