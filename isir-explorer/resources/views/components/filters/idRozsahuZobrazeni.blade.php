<div class="form-group row">
    <label for="idRozsahu" class="col-sm-2 col-form-label">Rozsah zobrazení</label>
    <div class="col-sm-10">
        <select name="idRozsahu" class="form-control" id="idRozsahu">
            @foreach ($rozsahyZobrazeni as $key => $item)
                <option value="{{$key}}" {{ Request::get('idRozsahu',0) == $key ? "selected" : "" }}>{{ $item['nazev'] }}</option>
            @endforeach
        </select>
    </div>
</div>
