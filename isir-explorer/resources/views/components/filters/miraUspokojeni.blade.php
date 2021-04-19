<div class="form-group row">
    <label for="miraUspokojeni" class="{{$classFormLabels}} col-form-label">Míra uspokojení</label>
    <div class="{{$classFormFields}}">
        @php
            $miraUspokojeni = [
                [0, "Skutečná"],
                [1, "Předpokládaná"],
                [2, "Rozdíl předpokládaná - skutečná"],
            ];
        @endphp
        <select name="miraUspokojeni" class="form-control" id="miraUspokojeni">
            @foreach ($miraUspokojeni as $item)
                <option value="{{$item[0]}}" {{ Request::get('miraUspokojeni') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
            @endforeach
        </select>
    </div>
</div>
