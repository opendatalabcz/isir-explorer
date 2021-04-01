import click


class AppConfig:

    DEFAULT_CONFIG_FILENAME = 'app.cfg'

    CONF_CATEGORIES = ['app', 'db', 'dl', 'ws', 'scraper']

    GLOBAL_CATEGORY = 'app'

    # Klice v nastaveni, ktere je vzdy nutne specifikovat
    REQUIRED = []

    CONVERT_INT = ['ws.min_id', 'ws.max_id', 'ws.retry_times', 'ws.last_id',
        'ws.concurrency', 'ws.request_timeout']

    # Vychozi hodnoty v nastaveni a popis konfigurace
    DEFAULTS = {
        # Globalni
        "tmp_dir": "/tmp/isir",                             # Adresar pro docasne soubory
        "debug": False,
        "verbose": False,
        "silent": False,

        # Scraper
        "scraper.pdftotext": "pdftotext",                        # Cesta ke spusteni programu pdftotext
        "scraper.pdftk": "pdftk",                                # Cesta ke spusteni programu pdftk
        "scraper.doctype": False,                                # Typ dokumentu, nespecifikovan => autodetekce
        "scraper.unpack_filter": "^D-DS-|^K-DS-",
        "scraper.save_unreadable": False,
        "scraper.save_text": False,
        "scraper.save_unpacked": False,
        "scraper._cli": False,

        # Isir ws
        "ws.last_id": None,
        "ws.min_id": None,
        "ws.max_id": None,
        "ws.retry_times": 5,
        "ws.concurrency": 4,
        "ws.request_timeout": 30,
        "ws.delay": 0,                                      # Zpozdeni v sekundach
        "ws.parse_in_executor": True,
        "ws.ins_filter": None,                              # Filtr na spisove znacky ins. rizeni,
                                                            # napr. "INS [0-9]+/20(19|20|20|21|22)"
        # Isir dl
        "dl.concurrency": 5,
        "dl.request_timeout": 300,
        "dl.retry_times": 3,
        "dl.keep_pdf": False,                               # Zachovat vsechny stazene pdf soubory, true/false/"log"
        "dl.limit": 0,                                      # Omezit počet dokumentů ke stažení
        "dl.delay": 3,                                      # Zpozdeni v sekundach
        "dl.delay_after": 100,                              # Po kolika dokumentech aplikovat zpozdeni
        "dl.start": 0,                                      # ID události v rejstříku, od které zahájit stahování
    }

    def __init__(self, conf=None):
        self.data = {}
        if conf:
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
                raise click.BadParameter(key + " je povinna hodnota nastaveni.")

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
