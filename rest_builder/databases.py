from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

_ENGINES = {}
_BASES = {}


def get_database_engine(user):
    """
    Gets a database engine from the _ENGINES
    dictionary.  Creates and inserts one if there
    isn't one available.

    :param rest_builder.models.User user: The user to get
        a database engine for that user's database
    :return: A sqlalchemy Engine instance corresponding
        to the user's database.
    :rtype: sqlalchemy.Engine
    """
    if user.id not in _ENGINES:
        user_database = 'sqlite:///{0}_user.db'.format(user.id)
        engine = create_engine(user_database)
        _ENGINES[user.id] = engine
    engine = _ENGINES[user.id]
    return engine


def get_declarative_base(user):
    """
    :param rest_builder.models.User user: The user to get
        a database engine for that user's database
    :return: An automapped base that reflects the user's
        database.
    :rtype: sqlalchemy.ext.declarative.Base
    """
    engine = get_database_engine(user)
    if user.id not in _BASES:
        base = automap_base()
        base.prepare(engine, reflect=True)
        _BASES[user.id] = base
    return _BASES[user.id]
