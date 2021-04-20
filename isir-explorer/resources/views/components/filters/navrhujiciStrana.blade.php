<div class="form-group row">
    <label for="navrhujiciStrana" class="{{$classFormLabels}} col-form-label">Navrhující strana</label>
    <div class="{{$classFormFields}}">
        @php
            $typOsoby = [
                ["IS", "Insolvenční správce"],
                ["DL", "Dlužník"],
            ];
        @endphp
        <select name="navrhujiciStrana" class="form-control" id="navrhujiciStrana">
            @foreach ($typOsoby as $item)
                <option value="{{$item[0]}}" {{ Request::get('navrhujiciStrana') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
            @endforeach
        </select>
    </div>
</div>
