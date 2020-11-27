Pdf scraper
===========

Součást projektu ISIR Explorer pro konverzu dat z pdf formulářů
zveřejňovaných v insolvenčním řízení do strukturované podoby.

Použití
-------

::

    Usage: scraper.py [OPTIONS] PDF_FILE

    Options:
      -o, --output FILENAME  Výstupní soubor nebo - pro stdout.  [default: -]
      -c, --config FILENAME  Cesta ke konfiguracnimu souboru.  [default: app.cfg]
      -d, --doctype TYPE     Výběr typu dokumentu. Podporovane hodnoty: Prihlaska,
                             PrehledovyList, ZpravaProOddluzeni,
                             ZpravaPlneniOddluzeni, ZpravaSplneniOddluzeni. Pokud
                             není zadáno, je použita automatická detekce dle
                             obsahu vstupního PDF souboru.

      -m, --multidoc         Aktivuje čtení více dokumentů z jednoho vstupního
                             PDF. Výstupem je pole objektů s nalezenými dokumenty.

      --debug                Debug výpis do stdout.
      --help                 Show this message and exit.

Instalace
---------

::

    git clone git@github.com:opendatalabcz/isir-explorer.git
    cd isir-explorer/pdf-scraper/
    python3.7 -m venv venv && . venv/bin/activate
    pip install .
    isir-scraper --help


Před použitím je nutné nastavit správnou cestu k upravenému programu
`pdftotext <https://github.com/opendatalabcz/poppler>`__ v konfiguračním
souboru.

Konfigurační soubor
-------------------

Aplikace hledá konfirační soubor v aktuálním adresáři nebo v umístění
specifikovaném přepínačem ``-c``/``--config``.
Příklad konfigurace je v *app.cfg.sample*.

Parametry:

-  **pdftotext** - Příkaz pro spuštení programu pdftotext (výchozí:
   *pdftotext*)
-  **tmp\_dir** - Adresář pro ukládání dočasných souborů při převodu
   (výchozí: */tmp/isir*)
