from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask.ext.user import current_user
from ripozo_sqlalchemy import AlchemyManager

from .models import ManagerModel, ResourceModel, Relationship, User, db


class UserFilteredManager(AlchemyManager):
    def queryset(self, session):
        return db.session.query(self.model).filter_by(owner=current_user)


class UserManager(AlchemyManager):
    fields = ('id', 'username', 'email', 'database_uri')
    model = User


class ResourceManager(UserFilteredManager):
    fields = ('id', 'model_name', 'links.id',)
    create_fields = ('model_name',)
    update_fields = ('model_name', 'links.id',)
    model = ResourceModel


class RelationshipManager(UserFilteredManager):
    fields = ('id', 'name', 'resource_id',)
    create_fields = ('name', 'resource_id',)
    update_fields = ('name', 'resource_id',)
    model = Relationship


class ManagerManager(UserFilteredManager):
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
