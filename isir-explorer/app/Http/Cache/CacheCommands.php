<?php

namespace App\Http\Cache;

use Illuminate\Foundation\Testing\Concerns\MakesHttpRequests;
use Illuminate\Support\Facades\URL;
use Tests\CreatesApplication;

class CacheCommands{

    use MakesHttpRequests, CreatesApplication;

    protected $app;

    const CACHED_ROUTES = [
        "stat.prehled.konkurz",
        "stat.prehled.reorg",
        "stat.prehled.oddluzeni",
        "spravci.ins",
        "veritele.ins",
    ];

    public function cacheStatistik($console){
        $res = ini_set('memory_limit', '1000M') && set_time_limit(600);

        if(!$res){
            $console->comment("Nepodarilo se nastavit memory_limit / max_execution_time!");
            $console->comment("Chache pro statistiky nebude vytvorena.");
            return;
        }
        $this->app = $this->createApplication();
        foreach (self::CACHED_ROUTES as $value) {
            $console->comment("=> " . $value);
            $this->get( URL::route($value, array(), false) );
        }
    }

}
