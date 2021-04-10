#!/bin/bash

# Sestaveni
docker-compose build

# Instalace PHP zavislosti
docker-compose run --rm isir_composer install

# Instalace JS zavislosti
docker-compose run --rm isir_npm install --cache /tmp

# Kompilace SASS, sestaveni a minifikace JS a CSS souboru
docker-compose run --rm isir_npm run prod

# Aktualizace nastaveni z .env
docker-compose run --rm isir_artisan config:clear

# Vytvoreni cache
docker-compose run --rm isir_artisan responsecache:statistiky

# Spusteni webserveru (ponechano na uzivateli)
# docker-compose up -d
