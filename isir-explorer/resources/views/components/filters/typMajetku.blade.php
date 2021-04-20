<div class="form-group row">
    <label for="typMajetku" class="{{$classFormLabels}} col-form-label">Typ majetku</label>
    <div class="{{$classFormFields}}">
        @php
            $typMajetku = App\Http\Controllers\Stats\OddlMajetekController::TYP_MAJETKU;
        @endphp
        <select name="typMajetku" class="form-control" id="typMajetku">
            @foreach ($typMajetku as $key => $item)
                <option value="{{$key}}" {{ Request::get('typMajetku') == $key ? "selected" : "" }}>{{ $item["nazev"] }}</option>
            @endforeach
        </select>
    </div>
</div>
