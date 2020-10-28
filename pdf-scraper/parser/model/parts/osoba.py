
class Osoba:
    def __init__(self, udaje):
        if hasattr(udaje, "Prijmeni"):
            self.FO_PO = 1
            self.Fyzicka_osoba = Fyzicka_osoba(udaje)
        else:
            self.FO_PO = 2
            self.Pravnicka_osoba = Pravnicka_osoba(udaje)


class Dluznik(Osoba):
    pass


class Veritel(Osoba):
    pass

class Adresa:
    pass

class UdajeOsoby:
    def __init__(self):
        self.Sidlo = Adresa()


class TypOsoby:
    def __init__(self, udaje):
        self.Udaje = udaje


class Fyzicka_osoba(TypOsoby):
    pass


class Pravnicka_osoba(TypOsoby):
    pass
