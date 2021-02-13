
class ImportException(Exception):
    """Obecná chyba importu.
    """
    pass


class UnknownDocument(ImportException):
    """Nepodařilo se rozpoznat typ importovaného dokumentu.
    """
    pass
