from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sqlalchemy import create_engine, Column, Integer, String, MetaData

import mock
import unittest2

from rest_builder.databases import (get_database_engine, get_declarative_base,
                                    _ENGINES, _BASES,)


class TestDatabaseHelpers(unittest2.TestCase):
    def setUp(self):
        self.uri = 'sqlite:///:memory:'
        self.metadata = MetaData()
        self.table = (
            'table', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('value', String(63)),
        )
        self.engine = create_engine(self.uri)
        self.metadata.create_all(self.engine)

    def test_get_database(self):
        user = mock.Mock(database_uri='sqlite:///:memory:')
        engine = get_database_engine(user)
        self.assertIn(self.uri, _ENGINES)
        self.assertIs(_ENGINES[self.uri], engine)
        engine2 = get_database_engine(user)
        self.assertIs(engine, engine2)
