<div class="form-group row">
    <label for="insZpusob" class="{{$classFormLabels}} col-form-label">Způsob řešení</label>
    <div class="{{$classFormFields}}">
        @php
            $insZpusob = [
                ["", "Všechny způsoby"],
                ["O", "Oddlužení"],
                ["K", "Konkurz"],
                ["R", "Reorganizace"],
            ];
        @endphp
        <select name="zpusobReseni" class="form-control" id="insZpusob">
            @foreach ($insZpusob as $item)
                <option value="{{$item[0]}}" {{ Request::get('zpusobReseni') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
            @endforeach
        </select>
    </div>
</div>
