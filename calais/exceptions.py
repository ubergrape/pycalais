"""
Exceptions related to OpenCalais.
"""
class CalaisError(Exception):
    """
    Base exception for errors returned by OpenCalais.
    """
    pass


class MaxQpsExceeded(CalaisError):
    """
    Exception raised when the maximum requests per seconds have been reached.
    """
    pass


class BusyCalais(CalaisError):
    """
    Exception raised when OpenCalais tells us that it is busy at the moment.
    """
    pass


class LanguageUnsupported(CalaisError):
    """
    Exception raised when the content language is not supported by OpenCalais.

    I've found out that this may also happen when you send some "unusual"
    content, like scores or lots of tabular data, to OpenCalais.
    """
    pass


class MaxLenExceeded(CalaisError):
    """
    Exception raised when too much content was tried to send to OpenCalais.

    I could not find a true limit. Some state that it is 100 000 characters,
    others say around 20-40kByte.
    """
    pass


class GatewayTimeout(CalaisError):
    """
    Exception raised when OpenCalais' Gateway timed out.
    """
    pass
