const mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix.js('resources/js/app.js', 'public/js')
    .sass('resources/sass/app.scss', 'public/css')
    .sourceMaps();

mix.js('resources/js/grafy.js', 'public/js');
mix.js('resources/js/maps.js', 'public/js');
mix.js('resources/js/detail-spravce.js', 'public/js');
mix.js('resources/js/detail-veritel.js', 'public/js');

// Pridani verzi pri nacitani frontend souboru (obnova cache po update)
mix.version();
