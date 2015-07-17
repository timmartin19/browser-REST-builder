from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask_sqlalchemy import SQLAlchemy

from ripozo import Relationship, ListRelationship, restmixins
from ripozo.resources.constructor import ResourceMetaClass
from ripozo_sqlalchemy import AlchemyManager, ScopedSessionHandler

from .databases import get_declarative_base, get_database_engine
from .exceptions import MissingModelException

import ujson

db = SQLAlchemy()

_RESTMIXINS_MAP = {
    'Create': restmixins.Create,
    'Retrieve': restmixins.Retrieve,
    'RetrieveList': restmixins.RetrieveList,
    'RetrieveRetrieveList': restmixins.RetrieveRetrieveList,
    'Update': restmixins.Update,
    'Delete': restmixins.Delete,
    'RetrieveUpdate': restmixins.RetrieveUpdate,
    'RetrieveUpdateDelete': restmixins.RetrieveUpdateDelete,
    'CreateRetrieve': restmixins.CreateRetrieveUpdate,
    'CreateRetrieveUpdate': restmixins.CreateRetrieveUpdate,
    'CRUD': restmixins.CRUD,
    'CRUDL': restmixins.CRUDL,
}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=31), unique=True)
    password = db.Column(db.String(length=63), nullable=False)
    email = db.Column(db.String(length=63), nullable=True)
    database_uri = db.Column(db.String, nullable=False, unique=True)
    resources = db.relationship('Resource', backref='owner')
    relationships = db.relationship('RelationshipModel', backref='owner')
    managers = db.relationship('Manager', backref='owner')


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    links = db.relationship('RelationshipModel')
    relationships = db.relationship('RelationshipModel')
    restmixin = db.Enum(*_RESTMIXINS_MAP.keys())
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=True)
    manager = db.relationship('Manager', backref='resources')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _pks = db.Column(db.Text, default='[]')

    def __init__(self, *args, **kwargs):
        # TODO docs
        super(Resource, self).__init__(*args, **kwargs)
        if not self.restmixin:
            self.restmixin = 'CRUDL'

    @property
    def pks(self):
        return ujson.loads(self._pks)

    @pks.setter
    def pks(self, value):
        self._pks = ujson.dumps(value)

    @property
    def resource_name(self):
        return '{0}{1}'.format(self.owner.username, self.manager.name)

    @property
    def restmixin_class(self):
        return _RESTMIXINS_MAP[self.restmixin]

    @property
    def resource(self):
        """
        :return: The ResourceBase subclass
            that this model represents
        :rtype: ripozo.ResourceBase
        """
        links = [rel.relationship for rel in self.links]
        relationships = [rel.relationship for rel in self.relationships]
        namespace = '/{0}'.format(self.owner.username)
        manager_class = self.manager.manager
        session = get_database_engine(self.owner)
        session_handler = ScopedSessionHandler(session)
        manager = manager_class(session_handler)
        attr_dict = dict(manager=manager, _links=links,
                         _relationships=relationships, namespace=namespace)
        return ResourceMetaClass(self.resource_name, (self.restmixin_class,), attr_dict)


class RelationshipModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    embedded = db.Column(db.Integer, default=False)
    is_list = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(length=63), nullable=False)
    no_pks = db.Column(db.Boolean, default=False)
    _query_args = db.Column(db.Text, default='[]')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _property_map = db.Column(db.Text, default='{}')
    relation = db.Column(db.String, nullable=False)
    required = db.Column(db.Integer, default=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))
    templated = db.Column(db.Boolean, default=False)

    @property
    def query_args(self):
        return ujson.loads(self._query_args)

    @query_args.setter
    def query_args(self, value):
        self._query_args = ujson.dumps(value)

    @property
    def property_map(self):
        return ujson.loads(self._property_map)

    @property_map.setter
    def property_map(self, value):
        self._property_map = ujson.dumps(value)

    @property
    def relationship(self):
        """
        :return: The Relationship or ListRelationship instance
            that this model represents.
        :rtype: ripozo.Relationship
        """
        if self.is_list:
            klass = ListRelationship
        else:
            klass = Relationship
        return klass(self.name, property_map=self.property_map, relation=self.relation,
                     embedded=self.embedded, required=self.required, no_pks=self.no_pks,
                     query_args=self.query_args, templated=self.templated)


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(length=31), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paginate_by = db.Column(db.Integer, default=20)
    _fields = db.Column(db.Text, default='[]')
    _create_fields = db.Column(db.Text, default='[]')
    _update_fields = db.Column(db.Text, default='[]')
    _list_fields = db.Column(db.Text, default='[]')

    @property
    def fields(self):
        return ujson.loads(self._fields)

    @fields.setter
    def fields(self, value):
        self._fields = ujson.dumps(value)

    @property
    def create_fields(self):
        return ujson.loads(self._create_fields)

    @create_fields.setter
    def create_fields(self, value):
        self._create_fields = ujson.dumps(value)

    @property
    def update_fields(self):
        return ujson.loads(self._update_fields)

    @update_fields.setter
    def update_fields(self, value):
        self._update_fields = ujson.dumps(value)

    @property
    def list_fields(self):
        return ujson.loads(self._list_fields)

    @list_fields.setter
    def list_fields(self, value):
        self._list_fields = ujson.dumps(value)

    @property
    def manager(self):
        """
        :return: AlchemyManager subclass
            that this model represents.
        :rtype: ripozo_sqlalchemy.AlchemyManager
        """
        attr_dict = dict(paginate_by=self.paginate_by,
                         model=self.model)
        if self.fields:
            attr_dict['fields'] = self.fields
        if self.create_fields:
            attr_dict['create_fields'] = self.create_fields
        if self.update_fields:
            attr_dict['update_fields'] = self.update_fields
        if self.list_fields:
            attr_dict['list_fields'] = self.list_fields
        return type(self.name, AlchemyManager, attr_dict)

    @property
    def name(self):
        return '{0}__{1}'.format(self.owner_id, self.model_name)

    @property
    def model(self):
        base = get_declarative_base(self.owner)
        if hasattr(base.classes, self.model_name):
            return getattr(base.classes, self.model_name)
        raise MissingModelException("The table with the name {0} does"
                                    "not exist in your database".format(self.model_name))
