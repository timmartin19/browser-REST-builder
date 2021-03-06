from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask_user import UserManager, SQLAlchemyAdapter
from flask_ripozo import FlaskDispatcher

from .models import db, User
from .resources import UserResource, ResourceResource, RelationshipResource

import click


def create_app(config=None):
    app = Flask('rest_builder')
    app.config.from_pyfile(config)
    manager = Manager(app)
    migrate = setup_db(app=app, manager=manager)
    register_resources(app)
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)
    return app, migrate, manager


def setup_db(app=None, manager=None):
    if app:
        db.init_app(app)
    migrate = Migrate(app=app, db=db)
    if manager:
        manager.add_command('db', MigrateCommand)
    return migrate


def register_resources(app):
    dispatcher = FlaskDispatcher(app, url_prefix='/api')
    dispatcher.register_resources(UserResource, RelationshipResource, ResourceResource)


@click.command()
def run_app():
    app = create_app(config='default_config.py')
    app.run(debug=True)


if __name__ == '__main__':
    run_app()
