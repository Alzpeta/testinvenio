# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 alzp.
#
# testInvenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio digital library framework."""

import os
import invenio_oaiserver.minters
from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('testinvenio', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='testinvenio',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='testinvenio Invenio',
    license='MIT',
    author='alzp',
    author_email='info@testinvenio.com',
    url='https://github.com/testinvenio/testinvenio',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'testinvenio = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'testinvenio_records = testinvenio.records:testInvenio',
            'authors = testinvenio.authors:Authors',
            'oarepo_actions = oarepo_actions:Actions'

        ],
        'invenio_base.blueprints': [
            'testinvenio = testinvenio.theme.views:blueprint',
            'testinvenio_records = testinvenio.records.views:blueprint',
            'testinvenio_deposit = testinvenio.deposit.views:blueprint',
        ],
        'invenio_assets.webpack': [
            'testinvenio_theme = testinvenio.theme.webpack:theme',
        ],
        'invenio_config.module': [
            'testinvenio = testinvenio.config',
        ],
        'invenio_i18n.translations': [
            'messages = testinvenio',
        ],
        'invenio_base.api_apps': [
            'testinvenio = testinvenio.records:testInvenio',
            'authors = testinvenio.authors:Authors',
            #'oarepo_actions = oarepo_actions:Actions'
        ],
        'invenio_jsonschemas.schemas': [
            'testinvenio = testinvenio.records.jsonschemas',
            'authors = testinvenio.authors.jsonschemas',
        ],
        'invenio_search.mappings': [
            'records = testinvenio.records.mappings',
            'authors = testinvenio.authors.mappings'
        ],
        'invenio_pidstore.fetchers': [
        'authid = testinvenio.authors.fetchers:author_pid_fetcher'
        ],
        'invenio_pidstore.minters': [
        'aminter = testinvenio.authors.minters:author_minter',
        'rminter = testinvenio.records.minters:minter'
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
