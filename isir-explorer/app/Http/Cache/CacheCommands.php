<?php

namespace App\Http\Cache;

use Illuminate\Foundation\Testing\Concerns\MakesHttpRequests;
use Illuminate\Support\Facades\URL;
use Tests\CreatesApplication;
use Tests\TestCase;

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
        $res = ini_set('memory_limit', '1000M');
        if(!$res){
            $console->comment("Nepodarilo se nastavit memory_limit!");
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
