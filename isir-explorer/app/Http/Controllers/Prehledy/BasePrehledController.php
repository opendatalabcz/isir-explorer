<?php

namespace App\Http\Controllers\Prehledy;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

abstract class BasePrehledController extends Controller
{

    public const ROK_PRO_PREHLEDY = 2020;

    abstract public function index(Request $request);
}

