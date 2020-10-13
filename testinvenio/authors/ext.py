# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for My site."""

from __future__ import absolute_import, print_function

from invenio_base.signals import app_loaded

from . import config
from invenio_oaiserver.models import OAISet
from invenio_db import InvenioDB
from invenio_indexer import InvenioIndexer
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch
from flask_celeryext import FlaskCeleryExt
from invenio_oaiserver import InvenioOAIServer
from invenio_oaiserver.views.server import blueprint
from invenio_db import db
from invenio_oaiserver.minters import OAIIDProvider


class Authors(object):
    """My site extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['testinvenio-authors'] = self
    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        for k in dir(config):
            if k.startswith('AUTHORS_'):
                app.config.setdefault(k, getattr(config, k))
            else:
                for n in ['RECORDS_REST_ENDPOINTS', 'RECORDS_REST_FACETS',
                          'RECORDS_REST_SORT_OPTIONS',
                          'RECORDS_REST_DEFAULT_SORT']:
                    if k == n:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))
