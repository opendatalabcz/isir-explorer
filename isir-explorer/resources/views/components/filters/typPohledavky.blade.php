<div class="form-group row">
    <label for="zobrazeniPo" class="col-sm-2 col-form-label">Typ pohledávky</label>
    <div class="col-sm-10">
        @php
            $typPohledavky = [
                ["", "Všechny typy"],
                ["N" , "Nezajištěná"],
                ["Z" , "Zajištěná"],
            ];
        @endphp
        <select name="typPohledavky" class="form-control" id="zobrazeniPo">
            @foreach ($typPohledavky as $item)
                <option value="{{$item[0]}}" {{ Request::get('typPohledavky', "") == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
            @endforeach
        </select>
    </div>
</div>
