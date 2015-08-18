from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask
from ripozo import Relationship, ListRelationship, ResourceBase, RequestContainer, restmixins
from ripozo.resources.constructor import ResourceMetaClass
from ripozo_sqlalchemy import ScopedSessionHandler, AlchemyManager

from rest_builder.models import db, RelationshipModel, ResourceModel, ManagerModel, User
from rest_builder.databases import _ENGINES, get_database_engine

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import unittest2


class TestModelConstruction(unittest2.TestCase):
    """
    This class is responsible for testing the construction
    of the various classes and instances from the database.
    It is primarily responsible for ensuring that Relationships,
    Resources, and Managers are properly constructed.
    """
    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
        db.init_app(app)
        self.app = app
        with app.app_context():
            db.create_all(app=app)
            self.db = db
            self.user = User(username='user', password='password',
                             database_uri='sqlite:///:memory:')
            db.session.add(self.user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
        self.engine = create_engine('sqlite:///:memory:')
        self.base = declarative_base()

        class Blah(self.base):
            __tablename__ = 'blah'
            id = Column(Integer, primary_key=True)

        self.model = Blah
        self.base.metadata.create_all(self.engine)
        _ENGINES['sqlite:///:memory:'] = self.engine

    def test_relationship_construction(self):
        """
        Tests a simple relationship construction
        """
        class Blah(ResourceBase):
            pks = ('blah',)

        rel_model = RelationshipModel(name='blah', property_map=dict(x='blah'),
                                      relation='Blah')
        rel = rel_model.relationship
        self.assertIsInstance(rel, Relationship)
        self.assertFalse(isinstance(rel, ListRelationship))
        res = rel.construct_resource(dict(x=1, y=2))
        self.assertIsInstance(res, Blah)
        self.assertEqual(res.url, '/blah/1')

    def test_list_relationship_construction(self):
        """
        Tests a simple ListRelationship construction
        from a database row.
        """
        class Blah(ResourceBase):
            pks = ('blah',)

        rel_model = RelationshipModel(name='blah', property_map=dict(x='blah'),
                                      relation='Blah', embedded=True)
        rel = rel_model.relationship
        self.assertIsInstance(rel, Relationship)
        self.assertFalse(isinstance(rel, ListRelationship))
        res = rel.construct_resource(dict(x=1, y=2))
        self.assertIsInstance(res, Blah)
        self.assertEqual(res.url, '/blah/1')

    def test_manager_construction(self):
        """
        Tests a simple Manager construction
        """
        with self.app.app_context():
            user = self.db.session.query(User).filter_by(username='user').first()
            man_model = ManagerModel(model_name='blah', owner=user, fields=('id',))
            manager = man_model.manager
            self.assertListEqual(manager.fields, ['id'])
            self.assertListEqual(manager.create_fields, ['id'])
            self.assertListEqual(manager.list_fields, ['id'])
            self.assertListEqual(manager.update_fields, ['id'])
            manager_instance = manager(ScopedSessionHandler(self.engine))
            self.assertIsInstance(manager_instance, AlchemyManager)
            blah_record = manager_instance.create({})
            blah_instance = Session(self.engine).query(self.model).get(blah_record.values())
            self.assertIsInstance(blah_instance, self.model)

    def test_resource_construction(self):
        """Simple Resource construction"""
        with self.app.app_context():
            user = self.db.session.query(User).filter_by(username='user').first()
            man_model = ManagerModel(model_name='blah', owner=user, fields=('id',))
            self.db.session.add(man_model)
            self.db.session.commit()
            res = ResourceModel(restmixin='CRUDL', manager=man_model, owner=user)
            res.pks = ['id']
            resource_class = res.resource
            self.assertEqual(restmixins.CRUDL, res.restmixin_class)
            self.assertIsInstance(resource_class, ResourceMetaClass)
            req = RequestContainer()
            resource_instance = resource_class.create(req)
            self.assertIsInstance(resource_instance, resource_class)
            id_ = resource_instance.properties['id']
            engine = get_database_engine(user)
            session = ScopedSessionHandler(engine).get_session()
            model = session.query(self.model).get(id_)
            self.assertIsNotNone(model)
