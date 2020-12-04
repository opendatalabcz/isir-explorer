
class DownloaderException(Exception):
    """Obecná chyba.
    """
    pass


class TooManyRetries(DownloaderException):
    """Prilis mnoho pokusu.
    """
    pass

