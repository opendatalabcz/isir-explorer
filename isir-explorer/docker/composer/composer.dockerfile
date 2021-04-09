FROM composer:2

RUN addgroup -g 1002 laravel && adduser -G laravel --uid 1002 -g laravel -s /bin/sh -D laravel

WORKDIR /var/www/html

