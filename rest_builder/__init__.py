from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rest_builder.app import create_app

import os

config_file = os.environ.get('REST_BUILDER_CONFIG', 'default_config.py')

app, migrate, manager = create_app(config=config_file)

if __name__ == '__main__':
    manager.run()