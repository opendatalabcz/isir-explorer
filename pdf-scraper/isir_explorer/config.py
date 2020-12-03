import click


class AppConfig:

    CONF_CATEGORIES = ['app', 'db']

    GLOBAL_CATEGORY = 'app'

    # Klice v nastaveni, ktere je vzdy nutne specifikovat
    REQUIRED = []

    CONVERT_INT = ['min_id', 'max_id', 'retry_times', 'last_id', 'concurrency', 'request_timeout']

    # Vychozi hodnoty v nastaveni a popis konfigurace
    DEFAULTS = {
        "pdftotext": "pdftotext",                           # Cesta ke spusteni programu pdftotext
        "tmp_dir": "/tmp/isir",                             # Adresar pro docasne soubory
        "doctype": False,                                   # Typ dokumentu, nespecifikovan => autodetekce
        "debug": False,

        # Isir ws
        "last_id": None,
        "min_id": None,
        "max_id": None,
        "retry_times": 5,
        "concurrency": 4,
        "request_timeout": 30,
        "verbose": False,
        "silent": False,
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
