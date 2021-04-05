<?php

use App\Http\Controllers\Maps\DluznikController;
use App\Http\Controllers\Maps\OddluzeniController;
use App\Http\Controllers\Maps\PocetInsolvenciController;
use App\Http\Controllers\Maps\PohledavkyController;
use App\Http\Controllers\Prehledy\KonkurzController;
use App\Http\Controllers\Prehledy\OddluzeniController as PrehledyOddluzeniController;
use App\Http\Controllers\Prehledy\ReorgController;
use App\Http\Controllers\SpravciController;
use App\Http\Controllers\StatController;
use App\Http\Controllers\Stats\OsobaController;
use App\Http\Controllers\Stats\PocetInsController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('index');
});

/** Zobrazeni detailnich statistik */
Route::get('/statistiky/vek_dluznika', [OsobaController::class, 'vek_detail'])
    ->name("stat.detail.dluznik.vek");
Route::get('/statistiky/typ_dluznika', [OsobaController::class, 'typOsoby_detail'])
    ->name("stat.detail.dluznik.typ");
Route::get('/statistiky/pocet_insolvenci', [PocetInsController::class, 'pocet_detail'])
    ->name("stat.detail.pocet");

/** Prehledove stranky */
Route::get('/statistiky/konkurz', [KonkurzController::class, 'index'])
    ->name("stat.prehled.konkurz");
Route::get('/statistiky/oddluzeni', [PrehledyOddluzeniController::class, 'index'])
    ->name("stat.prehled.oddluzeni");
Route::get('/statistiky/reorganizace', [ReorgController::class, 'index'])
    ->name("stat.prehled.reorg");

Route::get('/insolvence', [StatController::class, 'insolvence']);

Route::get('/mapy/kraje/insolvence', [PocetInsolvenciController::class, 'insolvence'])
    ->name("stat.mapy.ins");
Route::get('/mapy/kraje/insolvence_na_obyvatele', [PocetInsolvenciController::class, 'insolvenceNaObyvatele'])
    ->name("stat.mapy.ins.obyv");
Route::get('/mapy/kraje/prihlasene_pohledavky', [PohledavkyController::class, 'pohledavky'])
    ->name("stat.mapy.pohledavky");
Route::get('/mapy/kraje/vek_dluznika', [DluznikController::class, 'vek'])
    ->name("stat.mapy.dluznik.vek");
Route::get('/mapy/kraje/uspesnost_oddluzeni', [OddluzeniController::class, 'uspesnost'])
    ->name("stat.mapy.oddl.uspesnost");
Route::get('/mapy/kraje/zrusena_oddluzeni', [OddluzeniController::class, 'zrusena'])
    ->name("stat.mapy.oddl.zrusena");
Route::get('/mapy/kraje/vyse_osvobozeni', [OddluzeniController::class, 'osvobozeni'])
    ->name("stat.mapy.oddl.osvobozeni");

Route::get('/spravci', [SpravciController::class, 'list'])->name("spravci.ins");
Route::get('/spravci/{id}', [SpravciController::class, 'detail'])->name("spravci.detail");
Route::get('/spravci/{id}/odmeny', [SpravciController::class, 'odmeny'])->name("spravci.detail.odmeny");

Route::get('/mapy', function () {
    return view('maps');
});

Route::get('/1', function () {
    return view('welcome');
});

Route::get('/2', function () {
    return view('welcome2');
});
