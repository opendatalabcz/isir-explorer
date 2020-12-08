
class SpisovaZnacka:
    pass

class Pohledavka:

    def __init__(self):
        self.Vlastnosti = Vlastnosti()
        self.Vykonatelnost = False
        self.Vyse_jistiny = None

class Vykonatelnost:
    pass

class Prislusenstvi:
    pass

class Vlastnosti:
    """Vlastnosti pohledavky.
    """
    def __init__(self):
        self.Podrizena = False
        self.Splatna = False

class SplatnaOd:
    pass