
class ParserException(Exception):
    """Obecná chyba čtení dokumentu.
    """
    pass

class NoSplitterFound(ParserException):
    """Chyba, která nastane v případě, že není nalezen některý z kotvících řetězců,
    nutných pro dělení textu.
    """
    pass

class UnreadableDocument(ParserException):
    """Chyba, která nastane v případě, že ve vstupním textu se nepodaří nalézt
    očekávaný formát dokumentu.
    """
    pass

class IncompleteDocument(ParserException):
    """Chyba, která nastane v případě, že dokument se nepodařilo přečíst kompletní.
    """
    pass

class NotPdfPortfolio(Exception):
    """PDF soubor není archivem typu pdf-portfolio.
    """
    pass

class EmptyPdfPortfolio(Exception):
    """PDF soubor je archivem typu pdf-portfolio ale je prázdný, nebo neobsahuje žádné soubory
    po aplikaci filtru dle nastavení.
    """
    pass