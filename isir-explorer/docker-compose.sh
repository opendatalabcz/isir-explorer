#!/bin/bash
docker-compose build
docker-compose run --rm isir_composer install
docker-compose run --rm isir_npm install --cache /tmp
docker-compose run --rm isir_npm run prod
docker-compose run --rm isir_artisan config:clear
docker-compose run --rm isir_artisan responsecache:statistiky
docker-compose up
