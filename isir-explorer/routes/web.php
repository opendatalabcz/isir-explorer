<?php

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

Route::get('/mapy/kraje/insolvence', 'App\Http\Controllers\MapController@insolvence');
Route::get('/mapy/kraje/insolvence_na_obyvatele', 'App\Http\Controllers\MapController@insolvence_na_obyvatele');

Route::get('/mapy', function () {
    return view('maps');
});

Route::get('/1', function () {
    return view('welcome');
});

Route::get('/2', function () {
    return view('welcome2');
});
