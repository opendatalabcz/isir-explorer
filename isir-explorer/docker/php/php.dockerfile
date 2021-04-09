
FROM php:8.0.3-fpm-buster

ADD ./docker/php/www.conf /usr/local/etc/php-fpm.d/www.conf

RUN groupadd -g 1000 laravel && useradd -G laravel -g laravel -s /bin/sh laravel

RUN mkdir -p /var/www/html

RUN chown laravel:laravel /var/www/html

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y libpq-dev \
    && docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql \
    && docker-php-ext-install pdo pdo_pgsql pgsql

