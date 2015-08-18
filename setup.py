from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from setuptools import setup, find_packages

version = '0.1.0'


setup(
    author='Tim Martin',
    author_email='tim.martin@vertical-knowledge.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='A browser based client for building and visualizing REST API\'s with ripozo.',
    include_package_data=True,
    install_requires=[
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-User',
        'click',
        'flask-ripozo',
        'ripozo-sqlalchemy',
        'ujson',
    ],
    keywords='REST HATEOAS Hypermedia RESTful web API browser visualization',
    name='browser-rest-builder',
    packages=find_packages(exclude=['rest_builder_tests', 'rest_builder_tests.*']),
    tests_require=[
        'mock',
        'tox',
        'unittest2',
    ],
    test_suite='rest_builder_tests',
    version=version,
)

