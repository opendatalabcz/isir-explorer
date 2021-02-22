<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

/**
 * Class InsRizeni
 */
class InsRizeni extends Model
{
    protected $table = 'stat_vec';

    public $timestamps = false;

    protected $guarded = [];

    protected $dates = [
        'datum_zahajeni',
        'datum_upadku',
        'datum_zpusob_reseni',
        'datum_ukonceni',
    ];
}
