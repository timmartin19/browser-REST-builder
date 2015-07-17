from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class MissingModelException(Exception):
    """
    Raised when a a model_name on a model
    class does not exist in the database.
    """
