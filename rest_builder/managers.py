from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo_sqlalchemy import AlchemyManager

from .models import Resource, Relationship, User


class UserManager(AlchemyManager):
    fields = ('id', 'username', 'email', 'database_uri')
    model = User


class ResourceManager(AlchemyManager):
    fields = ('id', 'model_name', 'links.id',)
    create_fields = ('model_name',)
    update_fields = ('model_name', 'links.id',)
    model = Resource


class RelationshipManager(AlchemyManager):
    fields = ('id', 'name', 'resource_id',)
    create_fields = ('name', 'resource_id',)
    update_fields = ('name', 'resource_id',)
    model = Relationship
