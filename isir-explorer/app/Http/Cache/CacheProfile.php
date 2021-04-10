<?php

namespace App\Http\Cache;

use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Spatie\ResponseCache\CacheProfiles\BaseCacheProfile;
use Symfony\Component\HttpFoundation\Response;

class CacheProfile extends BaseCacheProfile
{
    public function shouldCacheRequest(Request $request): bool
    {
        return $request->isMethod('get');
    }

    public function shouldCacheResponse(Response $response): bool
    {
        if (! $this->hasCacheableResponseCode($response)) {
            return false;
        }

        if (! $this->hasCacheableContentType($response)) {
            return false;
        }

        return true;
    }

    public function hasCacheableResponseCode(Response $response): bool
    {
        if ($response->isSuccessful()) {
            return true;
        }

        if ($response->isRedirection()) {
            return true;
        }

        return false;
    }

    public function hasCacheableContentType(Response $response): bool
    {
        $contentType = $response->headers->get('Content-Type', '');

        if (str_starts_with($contentType, 'text/')) {
            return true;
        }

        if (Str::contains($contentType, ['/json', '+json'])) {
            return true;
        }

        return false;
    }
}
