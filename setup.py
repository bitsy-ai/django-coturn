#!/usr/bin/env python
import os
from typing import List

from setuptools import setup, find_packages
from django_coturn import __version__

long_description: str = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
install_requires = [
    'django>=3.2',
    'psycopg2'
]
python_requires = '>3.6.9'
setup(
    name = 'django_coturn',
    version = __version__,
    packages = find_packages(),
    author = 'Leigh Johnson',
    author_email = 'leigh@bitsy.ai',
    description = 'Django Coturn is a Django app to synchronize django admins/users with Coturn\'s user database. \
        Coturn is an open-source STUN/TURN/ICE server.',
    long_description = long_description,
    license = 'GNU AGPLv3',
    keywords = 'django stun turn ice coturn webrtc',
    url = 'http://github.com/bitsy-ai/django-coturn',
    classifiers = [],
    zip_safe = False,
    install_requires = install_requires,
    test_suite = 'pytest',
    python_requires=python_requires,
    include_package_data=True
)