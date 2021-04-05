<div class="form-group row">
    <label for="insObdobi" class="col-sm-2 col-form-label">
        @if(!empty($nazevVolbyObdobi))
            {{ $nazevVolbyObdobi }}
        @else
            Období zahájení řízení
        @endif
    </label>
    <div class="col-sm-10">
        <select name="obdobi" class="form-control" id="insObdobi">
            @if (!empty($obdobi->zahrnout_v_nabidce))
                <option value="" selected="">{{ $obdobi->obdobi_nazev }}</option>
            @elseif (!empty($povolitPrazdneObdobi))
                <option value="" @if(!empty($obdobi->nezvoleno))selected=""@endif>Nezvoleno</option>
            @endif

            @foreach ($varianty as $v)
                <option @if($v == $obdobi->obdobi_nazev)selected=""@endif>{{ $v }}</option>
            @endforeach
        </select>
    </div>
</div>
