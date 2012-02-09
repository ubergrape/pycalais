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
