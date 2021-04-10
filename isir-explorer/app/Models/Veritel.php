<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

/**
 * Class Spravce
 */
class Veritel extends Model
{
    protected $table = 'stat_veritel';

    public $timestamps = false;

    protected $guarded = [];

    protected $dates = [
        'posledni_ins',
    ];

    public function rizeni(){
        return $this->belongsToMany(InsRizeni::class, 'stat_veritel_ins', 'id_veritele', 'id_ins');
    }
}
