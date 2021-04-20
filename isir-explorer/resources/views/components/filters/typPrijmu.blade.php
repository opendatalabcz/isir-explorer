<div class="form-group row">
    <label for="typPrijmu" class="{{$classFormLabels}} col-form-label">Typ příjmu</label>
    <div class="{{$classFormFields}}">
        @php
            $typPrijmu = App\Http\Controllers\Stats\OddlPrijmyController::TYP_PRIJMU;
        @endphp
        <select name="typPrijmu" class="form-control" id="typPrijmu">
            @foreach ($typPrijmu as $key => $item)
                <option value="{{$key}}" {{ Request::get('typPrijmu') == $key ? "selected" : "" }}>{{ $item["nazev"] }}</option>
            @endforeach
        </select>
    </div>
</div>
