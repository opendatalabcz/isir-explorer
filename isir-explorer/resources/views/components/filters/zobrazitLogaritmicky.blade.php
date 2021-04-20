<div class="form-group row">
    <label for="zobrazeniTyp" class="{{$classFormLabels}} col-form-label">Typ zobrazení</label>
    <div class="{{$classFormFields}}">
        @php
            $poLetech = [
                ["lin", "Lineární"],
                ["log", "Logaritmické - osa " . ($vychoziLogOsa ?? "X")],
                ["logxy", "Logaritmické - osy X,Y"],
            ];
        @endphp
        <select name="zobrazeniTyp" class="form-control" id="zobrazeniPo">
            @foreach ($poLetech as $item)
                <option value="{{$item[0]}}" {{ Request::get('zobrazeniTyp', $vychoziZobrazeniTyp ?? null) == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
            @endforeach
        </select>
    </div>
</div>
