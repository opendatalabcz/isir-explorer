# IsirExplorer
IsirExplorer je webová aplikace pro prezentaci statistických dat z insolvenčního rejstříku. Aplikace slouží pouze pro prezentaci dat z existující databáze IsirExplorer. Pro vytvoření této databáze a její naplnění daty použijte [schema](https://github.com/opendatalabcz/isir-explorer/tree/master/schema) a [pdf-scraper](https://github.com/opendatalabcz/isir-explorer/tree/master/pdf-scraper).

## Instalace - docker
Aplikaci je možné nainstalovat pomocí nástroje docker-compose. Po naklonování repositáře lze pro instalaci postupovat takto:

1. Vytvoření konfiguračního souboru `.env`. Lze použít šablonu `.env.example`. V tomto souboru je nutné vyplnit údaje pro připojení k databázi, URL kde bude aplikace provozována (`APP_URL`) a API klíč ke službě Mapbox pro zobrazení mapového podkladu (`MAPBOX_KEY`).
2. Spustit `./docker-build.sh`, který obsahuje příkazy pro sestavení potřebných Docker kontejnerů dle `docker-compose.yml`.
3. `docker-compose up -d` v adresáři projektu spustí vytvořené kontejnery a služba bude dostupná portu specifikovaném v `docker-compose.yml` (ve výchozím stavu 8080)

V případě nutnosti aktualizace kontejnteru z aktuálních zdrojových souborů je nejdříve nutné použít příkaz `docker-compose down -v` pro odstranění datové jednotky skupiny kontejenerů. Následně pokračovat od kroku č. 2.

## Instalace - bez dockeru
Pro instalaci bez docker-compose je nunté mít nainstalované
* PHP 8.0 s rozšířením pdo_pgsql
* node >= 13.7
* composer

1. Vytvoření konfigurace `.env` stejně jako v případě instalace přes Docker
2. Spuštění následujících příkazů pro instalaci knihoven a kompilaci skriptů:
```
composer install
npm install
npm run prod
```
3. Nasměrování webserveru na cestu `/public` v adresáři projektu
