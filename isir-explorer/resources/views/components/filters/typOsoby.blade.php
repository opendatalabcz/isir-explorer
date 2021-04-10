<div class="form-group row">
    <label for="insDluznik" class="{{$classFormLabels}} col-form-label">Typ dlužníka</label>
    <div class="{{$classFormFields}}">
        @php
            $typOsoby = [
                ["", "Všechny typy"],
                ["FN", "Fyzická osoba - nepodnikatel"],
                ["FP", "Fyzická osoba - podnikatel"],
                ["P", "Právnická osoba"],
            ];
        @endphp
        <select name="typOsoby" class="form-control" id="insDluznik">
            @foreach ($typOsoby as $item)
                @if(!in_array($item[0], $vyraditTypOsoby))
                    <option value="{{$item[0]}}" {{ Request::get('typOsoby') == $item[0] ? "selected" : "" }}>{{ $item[1] }}</option>
                @endif
            @endforeach
        </select>
    </div>
</div>
