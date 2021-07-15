@extends('layouts.app')

@section('content')

<div class="container mainpage">
    <div class="row">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <h1>IsirExplorer</h1>
                </div>
                <div class="card-body">
                    <p>
                        IsirExplorer umožňuje sběr a následné zobrazení agregovaných dat o insolvencích v ČR.
                        Tento web slouží k prezentaci získaných dat a statistik.
                        Projekt je určen veřejnosti pro poskytnutí přehledu o stavu insolvenčního procesu v ČR.
                    </p>

                    <div class="row">
                        <div class="col-xl-8">
                            <h2>Insolvenční řízení</h2>
                            <p>
                                Insolvenční řízení je zvláštní druh soudního řízení, jehož předmětem je dlužníkův úpadek a způsoby jeho řešení. Základním cílem insolvenčního řízení je uspořádaní majetkových vztahů mezi dlužníkem a jeho věřiteli. V České republice se tento proces v současné právní úpravě řídí zejména zákonem 182/2006 Sb., o úpadku a způsobech jeho řešení (insolvenční zákon).
                            </p>
                            <p>
                                Insolvenční zákon uvádí 4 možné způsoby řešení úpadku: konkurs, reorganizace, oddlužení a zvláštní způsoby pro určité subjekty nebo druhy případů stanovené zákonem. IsirExplorer se při sběru a&nbsp;prezentaci dat zaměřuje na insolvence řešící úpadek dlužníka formou oddlužení.
                            </p>

                            <h2>Dostupné statistiky</h2>
                                <ul>
                                <li><p>Sekce <a href="{{ route("veritele.ins") }}">Věřitelé</a> obsahuje informace o nejčastejších věřitelích vyskytujících se v insolvenčních řízeních. U každého věřitele je možné zobrazit detail, jako je průměrná výše přihlášky, nejčastejší typy insolvencí a kraje dlužníků.</p></li>
                                <li><p>Sekce <a href="{{ route("spravci.ins") }}">Správci</a> poskytuje seznam insolvenčních správců, možnost srovnávat velikosti spravovaných insolvencí nebo informace o odměnách správců z oddlužení.</p></li>
                                <li><p>V kategorii <a href="{{ route("stat.mapy.ins") }}">Mapy</a> je možné srovnávat vybrané statistické údaje o insolvencích mezi jednotlivými kraji v ČR. Je možné srovnávat údaje jako počty insolvencí, podíl populace kraje v insolvenci, průměrný věk dlužníka aj.</p></li>
                                <li><p>Sekce <a href="{{ route("stat.prehled.ins") }}">Statistiky</a> obsahuje přehledová data prezentovaná formou grafů a to celkově pro všechny insolvence nebo jen pro konkrétní formu řešení úpadku. Pro každý graf je možné zobrazit detail a konfigurovat parametry výstupu, jako jsou časový úsek dat, typ osoby dlužníka, způsob řešení úpadku atp.</p></li>
                                </ul>
                            </p>
                        </div>
                        <div class="col-xl-4 isir-ex-img-wrap">
                            <div class="isir-ex-img">
                            <img class="img1" alt="Uspesnost oddluzeni" src="/img/screens/uspesnost-oddluzeni.png">
                            <img class="img2" alt="Pocet insolvenci" src="/img/screens/pocet-ins.png">
                            <img class="img3" alt="Statistiky oddluzeni" src="/img/screens/stat-oddluzeni.png">
                            </div>
                        </div>
                    </div>

                    <h2>Zdroje dat</h2>
                    <p>
                        Data jsou získávána automatizovaným čtením PDF dokumentů zveřejňovaných v insolvenčním rejstříku. Doplňujícím zdrojem dat je databáze insolvenčního rejstříku poskytovaná formou webové služby Ministerstvem spravedlnosti ČR.
                    </p>
                    <p>
                        V případě automatizovaného čtení dat z insolvenčních dokumentů se často nepodaří přečíst 100% dokumentů u všech řízení (např. z důvodu neznámého formátu formuláře, naskenovaného dokumentu, atp.), a proto prezentované absolutní hodnoty mohou být nižší, než je tomu ve skutečnosti.
                        Při interpretaci statistik využívajících těchto dat je tedy nutné dbát na to, že zahrnují pouze část všech insolvenčních řízení. U většiny výstupů je však tento vzorek dat dostatečně velký na to, aby výsledné statistiky poskytovaly reprezentativní informace v dlouhodobých průměrech, při relativních srovnáních mezi kraji, časovými úseky atd.
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

@endsection
