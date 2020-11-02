# Pdf scraper
Součást projektu ISIR Explorer pro konverzu dat z pdf formulářů zveřejňovaných v insolvenčním řízení do strukturované podoby.

## Použití

```
Usage: scraper.py [OPTIONS] PDF_FILE

Options:
  --debug                Aktivuje debug vypis do stdout.
  -c, --config FILENAME  Cesta ke konfiguracnimu souboru aplikace.  [default:
                         app.cfg; required]

  --help                 Show this message and exit.
```

## Instalace

```
git clone git@github.com:opendatalabcz/isir-explorer.git
cd pdf-scraper
pip install -r requirements.txt
python3 scraper.py
```

TODO: K dispozici bude instalace přes `pip install`

## Konfigurační soubor

Aplikace hledá konfirační soubor v aktuálním adresáři nebo v umístění specifikovaném přepínačem `-c`/`--config`.
Příklad konfigurace je v *app.cfg.sample*.

Parametry:
* **pdftotext** - Příkaz pro spuštení programu pdftotext (výchozí: *pdftotext*)
* **tmp_dir** - Adresář pro ukládání dočasných souborů při převodu (výchozí: */tmp/isir*)