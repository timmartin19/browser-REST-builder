from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=31), unique=True)
    password = db.Column(db.String(length=63), nullable=False)
    email = db.Column(db.String(length=63), nullable=True)
    database_uri = db.Column(db.String, nullable=False)


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(length=31), nullable=False)
    links = db.relationship('Relationship', backref='resource')


class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=63), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))


class FlaskSQLAlchemySessionHandler(object):
    @staticmethod
    def get_session(self):
        return db.session

    @staticmethod
    def handle_session(session, exc=None):
        if exc:
            session.rollback()
