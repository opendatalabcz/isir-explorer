

class Dluznik:
    def __init__(self):
        self.FO_PO = 1
        self.Fyzicka_osoba = Fyzicka_osoba()
        self.Pravnicka_osoba = Pravnicka_osoba()


class Veritel:
    def __init__(self):
        self.FO_PO = 2
        self.Fyzicka_osoba = Fyzicka_osoba()
        self.Pravnicka_osoba = Pravnicka_osoba()


class UdajeOsoby:
    pass


class Osoba:
    pass


class Fyzicka_osoba(Osoba):
    def __init__(self):
        self.Udaje = UdajeOsoby()


class Pravnicka_osoba(Osoba):
    def __init__(self):
        self.Udaje = UdajeOsoby()
