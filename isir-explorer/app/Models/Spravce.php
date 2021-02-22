<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

/**
 * Class Spravce
 */
class Spravce extends Model
{
    protected $table = 'stat_spravce';

    public $timestamps = false;

    protected $guarded = [];

    public function rizeni(){
        return $this->belongsToMany(InsRizeni::class, 'stat_spravce_ins', 'id_spravce', 'id_ins');
    }
}
