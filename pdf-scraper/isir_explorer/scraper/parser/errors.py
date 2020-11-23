
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
