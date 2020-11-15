
class ParserException(Exception):
    pass

class NoSplitterFound(ParserException):
    pass

class UnreadableDocument(ParserException):
    pass
