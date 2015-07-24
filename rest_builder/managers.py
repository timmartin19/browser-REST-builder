from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo_sqlalchemy import AlchemyManager

from .models import ManagerModel, ResourceModel, Relationship, User, db


class UserManager(AlchemyManager):
    fields = ('id', 'username', 'email', 'database_uri')
    model = User


class ResourceManager(AlchemyManager):
    fields = ('id', 'model_name', 'links.id',)
    create_fields = ('model_name',)
    update_fields = ('model_name', 'links.id',)
    model = ResourceModel


class RelationshipManager(AlchemyManager):
    fields = ('id', 'name', 'resource_id',)
    create_fields = ('name', 'resource_id',)
    update_fields = ('name', 'resource_id',)
    model = Relationship


class ManagerManager(AlchemyManager):
    fields = ('id', 'name', 'resources.id')
    create_fields = ('name', 'resources.id')
    update_fields = ('name', 'resources.id')
    model = ManagerModel


class FlaskSQLAlchemySessionHandler(object):
    @staticmethod
    def get_session(self):
        return db.session

    @staticmethod
    def handle_session(session, exc=None):
        if exc:
            session.rollback()
