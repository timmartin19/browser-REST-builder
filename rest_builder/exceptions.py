from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo.exceptions import RestException


class MissingModelException(RestException):
    """
    Raised when a a model_name on a model
    class does not exist in the database.
    """


class UnauthenticatedException(RestException):
    """Raised when the user is not authenticated"""
    def __init__(self, status_code=401, *args, **kwargs):
        super(UnauthenticatedException, self).__init__(status_code=status_code, *args, **kwargs)


class UnauthorizedException(RestException):
    """Raised when the user is not authorized"""
    def __init__(self, status_code=403, *args, **kwargs):
        super(UnauthorizedException, self).__init__(status_code=status_code, *args, **kwargs)
