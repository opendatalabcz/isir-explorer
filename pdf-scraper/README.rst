Pdf scraper
===========

Součást projektu ISIR Explorer pro extrakci dat z pdf formulářů
zveřejňovaných v insolvenčním řízení do strukturované podoby.

Použití
-------

::

    Usage: isir-scraper [OPTIONS] PDF_FILE

    Options:
      -o, --output FILENAME  Výstupní soubor nebo - pro stdout.  [default: -]
      -c, --config FILENAME  Cesta ke konfiguracnimu souboru.
      -d, --doctype TYPE     Výběr typu dokumentu. Podporovane hodnoty: Prihlaska,
                             PrehledovyList,
                             ZpravaProOddluzeni,ZpravaPlneniOddluzeni,
                             ZpravaSplneniOddluzeni. Pokud není zadáno, je použita
                             automatická detekce dle obsahu vstupního PDF souboru.

      -m, --multidoc         Aktivuje čtení více dokumentů z jednoho vstupního
                             PDF. Výstupem je pole objektů s nalezenými dokumenty.

      --save-text            Do dočasného adresáře bude zapsána dekódovaná textová
                             podoba PDF formuláře.

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

Po dokončení instalace budou v prostředí kromě nástroje isir-scraper také nástroje isir-ws, isir-dl, isir-importer a isir-stats. Nápovědu každého z nich lze zobrazit spuštěním vybraného nástroje s přepínačem --help.

Konfigurační soubor
-------------------

Aplikace hledá konfirační soubor v aktuálním adresáři nebo v umístění
specifikovaném přepínačem ``-c``/``--config``.
Příklad konfigurace je v *app.cfg.sample*.
Konfigurační soubor je členěn do kategorií dle oblasti, pro která jsou nastavení aplikována. Možné kategorie jsou app (globální), db (databáze), dl (stahování), ws (webservice), scraper (nástroj pro čtení PDF).

Globální parametry:
-  **app.tmp\_dir** - Adresář pro ukládání dočasných souborů při převodu
   (výchozí: */tmp/isir*)
-  **app.debug** - Aktivace testovacích výpisů u nástrojů, které to umožňují
   (výchozí: *False*)
-  **app.verbose** - Aktivace vyšších detailů u výpisů
   (výchozí: *False*)
-  **app.silent** - Deaktivace stavových výstupů nástroje
   (výchozí: *False*)

Parametry specifické pro scraper:
-  **scraper.pdftotext** - Příkaz pro spuštení programu pdftotext
   (výchozí: *pdftotext*)
-  **scraper.pdftk** - Příkaz pro spuštení programu pdftk
   (výchozí: *pdftk*)
-  **scraper.save_unreadable** - Možnost aktivace ukládání nečitelných souborů
   (výchozí: *False*)
-  **scraper.save_text** - Možnost aktivace ukládání textového obsahu PDF
   (výchozí: *False*)
-  **scraper.save_unpacked** - Možnost aktivace ukládání obsahu pdf kolekcí
   (výchozí: *False*)

Kompletní seznam možných konfiguračních hodnot je v souboru config.py.
