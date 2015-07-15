from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo import restmixins

from .managers import (UserManager, RelationshipManager, ResourceManager,
                       FlaskSQLAlchemySessionHandler,)


class UserResource(restmixins.CRUDL):
    pks = ('id',)
    manager = UserManager(FlaskSQLAlchemySessionHandler)


class ResourceResource(restmixins.CRUDL):
    pks = ('id',)
    manager = ResourceManager(FlaskSQLAlchemySessionHandler)


class RelationshipResource(restmixins.CRUDL):
    pks = ('id',)
    manager = RelationshipManager(FlaskSQLAlchemySessionHandler)
