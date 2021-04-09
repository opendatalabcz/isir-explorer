FROM nginx:stable-alpine

ADD ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
ADD ./docker/nginx/default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /var/www/html

RUN addgroup -g 1002 laravel && adduser --uid 1002 -G laravel -g laravel -s /bin/sh -D laravel

RUN chown laravel:laravel /var/www/html
