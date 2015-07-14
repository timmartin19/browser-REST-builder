from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask
from rest_builder.models import db

import click


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    return app


@click.command()
def run_app():
    app = create_app(config='rest_builder.default_config')
    app.run(debug=True)


if __name__ == '__main__':
    run_app()
