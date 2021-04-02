<?php

use App\Http\Controllers\Maps\PocetInsolvenciController;
use App\Http\Controllers\Maps\PohledavkyController;
use App\Http\Controllers\SpravciController;
use App\Http\Controllers\StatController;
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

Route::get('/insolvence', [StatController::class, 'insolvence']);

Route::get('/mapy/kraje/insolvence', [PocetInsolvenciController::class, 'insolvence'])
    ->name("stat.mapy.ins");
Route::get('/mapy/kraje/insolvence_na_obyvatele', [PocetInsolvenciController::class, 'insolvenceNaObyvatele'])
    ->name("stat.mapy.ins.obyv");
Route::get('/mapy/kraje/prihlasene_pohledavky', [PohledavkyController::class, 'pohledavky'])
    ->name("stat.mapy.pohledavky");

Route::get('/spravci', [SpravciController::class, 'list'])->name("spravci.ins");
Route::get('/spravci/{id}', [SpravciController::class, 'detail'])->name("spravci.detail");

Route::get('/mapy', function () {
    return view('maps');
});

Route::get('/1', function () {
    return view('welcome');
});

Route::get('/2', function () {
    return view('welcome2');
});
