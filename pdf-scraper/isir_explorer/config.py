import click


class AppConfig:

    CONF_CATEGORIES = ['app', 'db', 'dl']

    GLOBAL_CATEGORY = 'app'

    # Klice v nastaveni, ktere je vzdy nutne specifikovat
    REQUIRED = []

    CONVERT_INT = ['min_id', 'max_id', 'retry_times', 'last_id', 'concurrency', 'request_timeout']

    # Vychozi hodnoty v nastaveni a popis konfigurace
    DEFAULTS = {
        # Globalni
        "tmp_dir": "/tmp/isir",                             # Adresar pro docasne soubory
        "debug": False,

        # Scraper
        "pdftotext": "pdftotext",                           # Cesta ke spusteni programu pdftotext
        "pdftk": "pdftk",                                   # Cesta ke spusteni programu pdftk
        "doctype": False,                                   # Typ dokumentu, nespecifikovan => autodetekce
        "unpack_filter": "^D-DS-|^K-DS-",
        "save_unreadable": True,
        "sc.save_text": False,
        "sc.save_unpacked": False,
        "sc._cli": False,

        # Isir ws
        "last_id": None,
        "min_id": None,
        "max_id": None,
        "retry_times": 5,
        "concurrency": 4,
        "request_timeout": 30,
        "verbose": False,
        "silent": False,
        "parse_in_executor": True,
        "ins_filter": None,                                 # Filtr na spisove znacky ins. rizeni, napr. "INS [0-9]+/20(19|20|20|21|22)"

        "dl.concurrency": 5,
        "dl.request_timeout": 300,
        "dl.retry_times": 3,
        "dl.keep_pdf": False,                               # Zachovat vsechny stazene pdf soubory, true/false/"log"
        "dl.limit": 0,                                      # Omezit počet dokumentů ke stažení
        "dl.delay": 3,                                      # Zpozdeni v sekundach
        "dl.delay_after": 100,                              # Po kolika dokumentech aplikovat zpozdeni
    }

    def __init__(self, conf):
        self.data = {}
        self.init(conf)
        self.validate_required()
        self.set_defaults()
        self.validate_fields()

    def init(self, conf):
        sections = conf.sections()
        for section in sections:
            if section in self.CONF_CATEGORIES:
                self.configuration_section(conf, section)

    def configuration_section(self, conf, section):
        conf_items = conf[section]
        prefix = section + "."
        if section == self.GLOBAL_CATEGORY:
            prefix = ""
        for key in conf_items:
            self.data[prefix + key] = conf_items[key]

    def validate_required(self):
        for key in self.REQUIRED:
            if key not in self.data:
                raise click.BadParameter(key+" je povinna hodnota nastaveni.")

    def set_defaults(self):
        for key in self.DEFAULTS:
            if key not in self.data:
                self.data[key] = self.DEFAULTS[key]

    def validate_fields(self):
        for key in self.CONVERT_INT:
            if self.data[key] is None:
                continue
            try:
                self.data[key] = int(self.data[key])
            except ValueError:
                raise click.BadParameter(key + " musi byt cislo.")

    def set_opt(self, key, val):
        if val is None:
            return
        self.data[key] = val

    def __setitem__(self, key, data):
        self.data[key] = data

    def __getitem__(self, key):
        return self.data[key]
