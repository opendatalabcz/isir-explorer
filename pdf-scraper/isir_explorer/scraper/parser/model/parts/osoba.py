
class Osoba:
    def __init__(self, udaje):
        if hasattr(udaje, "Prijmeni"):
            self.FO_PO = 1
            self.Fyzicka_osoba = Fyzicka_osoba(udaje)
        else:
            self.FO_PO = 2
            self.Pravnicka_osoba = Pravnicka_osoba(udaje)

    def __repr__(self):
        if self.FO_PO == 1:
            return self.Fyzicka_osoba.__repr__()
        else:
            return self.Pravnicka_osoba.__repr__()

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

    def __repr__(self):
        return self.Udaje.Prijmeni


class Pravnicka_osoba(TypOsoby):

    def __repr__(self):
        return self.Udaje.Nazev+'-'+self.Udaje.IC
