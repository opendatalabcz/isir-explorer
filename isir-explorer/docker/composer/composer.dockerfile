FROM composer:2

RUN addgroup -g 1000 laravel && adduser -G laravel -g laravel -s /bin/sh -D laravel

WORKDIR /var/www/html

ADD ./composer.json /var/www/html/composer.json
ADD ./composer.lock /var/www/html/composer.lock
RUN composer config -g use-github-api false
RUN composer config -g preferred-install dist
RUN composer config -g disable-tls true
RUN composer --ignore-platform-reqs install
