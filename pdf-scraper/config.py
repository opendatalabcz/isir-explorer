import click


class AppConfig:

    CONF_CATEGORIES = ['app']

    GLOBAL_CATEGORY = 'app'

    # Klice v nastaveni, ktere je vzdy nutne specifikovat
    REQUIRED = []

    # Vychozi hodnoty v nastaveni a popis konfigurace
    DEFAULTS = {
        "pdftotext": "pdftotext",                           # Cesta ke spusteni programu pdftotext
        "tmp_dir": "/tmp/isir",                             # Adresar pro docasne soubory
        "debug": False,
    }

    def __init__(self, conf):
        self.data = {}
        self.init(conf)
        self.validate_required()
        self.set_defaults()

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

    def set_opt(self, key, val):
        if val is None:
            return
        self.data[key] = val

    def __setitem__(self, key, data):
        self.data[key] = data

    def __getitem__(self, key):
        return self.data[key]
