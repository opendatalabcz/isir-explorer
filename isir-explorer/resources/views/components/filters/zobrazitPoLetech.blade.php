<div class="form-group row">
    <label for="zobrazeniPo" class="{{$classFormLabels}} col-form-label">Zobrazení</label>
    <div class="{{$classFormFields}}">
        @php
            $poLetech = [
                [0, "Po měsících"],
                [1, "Po letech"],
            ];
        @endphp
        <select name="poLetech" class="form-control" id="zobrazeniPo">
            @foreach ($poLetech as $item)
                <option value="{{$item[0]}}" {{ Request::get('poLetech') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
            @endforeach
        </select>
    </div>
</div>
