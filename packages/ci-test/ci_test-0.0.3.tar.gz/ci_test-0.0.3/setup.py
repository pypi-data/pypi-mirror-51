#!/usr/bin/env python

import os

from setuptools import setup, find_packages

version = os.environ.get('VERSION')
if version is None:
    with open(os.path.join('.', 'VERSION')) as version_file:
        version = version_file.read().strip()

with open('requirements.txt') as requirements:
    requires = list(requirements)

setup_options = {
    'name': 'ci_test',
    'version': version,
    'description': 'ci_test',
    'author': 'GwangwonChoi',
    'author_email': 'rhkddnjs99@hotmail.com',
    'packages': find_packages(exclude=['tests*', 'docs']),
    'include_package_data': True,
    'py_modules': ['ci_test'],
    'license': "Apache License 2.0",
    'install_requires': requires,
    'test_suite': 'tests',
    'entry_points': {
        'console_scripts': [
            'citest=ci_test:main'
        ],
    },
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6'
    ]
}

setup(**setup_options)
