<?php

use App\Http\Controllers\MapController;
use App\Http\Controllers\SpravciController;
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

Route::get('/mapy/kraje/insolvence', [MapController::class, 'insolvence'])->name("stat.mapy");
Route::get('/mapy/kraje/insolvence_old', [MapController::class, 'insolvence2']);
Route::get('/mapy/kraje/insolvence_na_obyvatele', [MapController::class, 'insolvence_na_obyvatele']);

Route::get('/spravci', [SpravciController::class, 'list'])->name("spravci");
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
