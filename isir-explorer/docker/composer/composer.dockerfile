FROM composer:2

RUN addgroup -g 1002 laravel && adduser -G laravel --uid 1002 -g laravel -s /bin/sh -D laravel

RUN mkdir -p /var/www/html

WORKDIR /var/www/html

COPY . /var/www/html

RUN chown laravel:laravel /var/www/html
