<?php

namespace App\Providers;

use Illuminate\Routing\UrlGenerator;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Blade;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        \Carbon\Carbon::setLocale(config('app.locale'));
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::directive('isir_link', function ($spis) {
            return "<?php echo getInsLink($spis); ?>";
        });

        if (!App::environment('local')) {
            URL::forceRootUrl(config('app.url'));
            URL::forceScheme('https');
        }
    }
}
