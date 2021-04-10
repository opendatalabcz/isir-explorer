<div class="form-group row">
    <label for="idRozsahu" class="{{$classFormLabels}} col-form-label">Rozsah zobrazení</label>
    <div class="{{$classFormFields}}">
        <select name="idRozsahu" class="form-control" id="idRozsahu">
            @foreach ($rozsahyZobrazeni as $key => $item)
                <option value="{{$key}}" {{ Request::get('idRozsahu',0) == $key ? "selected" : "" }}>{{ $item['nazev'] }}</option>
            @endforeach
        </select>
    </div>
</div>
