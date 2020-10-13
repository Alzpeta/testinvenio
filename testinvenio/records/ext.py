# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 alzp.
#
# testInvenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for testInvenio."""

from __future__ import absolute_import, print_function

import pathlib

import pkg_resources
from invenio_base.signals import app_loaded
from invenio_files_rest.signals import file_deleted, file_uploaded
from invenio_indexer.signals import before_record_index

from . import config, indexer
import json
from .tasks import update_record_files_async
from invenio_db import InvenioDB
from invenio_indexer import InvenioIndexer
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch
from flask_celeryext import FlaskCeleryExt
from invenio_oaiserver import InvenioOAIServer
from invenio_oaiserver.views.server import blueprint
from invenio_db import db
from invenio_oaiserver.models import OAISet

from invenio_oaiserver.minters import OAIIDProvider


def oai_server(sender, app=None, **kwargs):
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['CELERY_TASK_ALWAYS_EAGER'] = True
    if not hasattr(app, 'cli'):
        from flask_cli import FlaskCLI
        ext_cli = FlaskCLI(app)
    ext_db = InvenioDB(app)
    ext_indexer = InvenioIndexer(app)
    ext_pidstore = InvenioPIDStore(app)
    ext_records = InvenioRecords(app)
    ext_search = InvenioSearch(app)
    ext_celery = FlaskCeleryExt(app)
    app.config['OAISERVER_RECORD_INDEX'] = ['authors', 'records']
    app.config['OAISERVER_ID_PREFIX'] = 'oai:example:'
    app.config['OAISERVER_QUERY_PARSER_FIELDS'] = ["title"]
    app.config['OAISERVER_METADATA_FORMATS'] = {'oai_dc':{
            'serializer': (
                'invenio_oaiserver.utils:dumps_etree', {
                    'xslt_filename': pkg_resources.resource_filename(
                        'testinvenio.records', 'static/xsl/MARC21slim2OAIDC.xsl'
                    ),
                    'xslt_filename': pathlib.Path("/home/alzbeta/testinvenio/testinvenio/records/static/xsl/MARC21slim2OAIDC.xsl")
                }
            ),
            'schema': 'http://json-schema.org/draft-04/schema#',
            'namespace': 'http://json-schema.org/draft-04/schema#',
        }}

    ext_oaiserver = InvenioOAIServer(app)
    app.register_blueprint(blueprint)
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    ext_search.flush_and_refresh('_all')
    oaiset = OAISet(spec='pattern', name='Pattern', description='...')
    #nefunguje pokud search pattern ma pole ktere neni v obouch modelech...
    oaiset.search_pattern = 'title:Some title1'
    try:
        print("1")
        db.session.add(oaiset)
        db.session.commit()
    except:
        pass

class testInvenio(object):
    """testInvenio extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)


    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['testinvenio'] = self
        app_loaded.connect(oai_server)
        self._register_signals(app)



    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        with_endpoints = app.config.get(
            'TESTINVENIO_ENDPOINTS_ENABLED', True)
        for k in dir(config):
            if k.startswith('TESTINVENIO_'):
                app.config.setdefault(k, getattr(config, k))
            elif k == 'SEARCH_UI_JSTEMPLATE_RESULTS':
                app.config['SEARCH_UI_JSTEMPLATE_RESULTS'] = getattr(
                    config, k)
            elif k == 'PIDSTORE_RECID_FIELD':
                app.config['PIDSTORE_RECID_FIELD'] = getattr(config, k)
            elif k == 'FILES_REST_PERMISSION_FACTORY':
                app.config['FILES_REST_PERMISSION_FACTORY'] =\
                        getattr(config, k)
            else:
                for n in ['RECORDS_REST_ENDPOINTS', 'RECORDS_UI_ENDPOINTS',
                          'RECORDS_REST_FACETS', 'RECORDS_REST_SORT_OPTIONS',
                          'RECORDS_REST_DEFAULT_SORT',
                          'RECORDS_FILES_REST_ENDPOINTS']:
                    if k == n and with_endpoints:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))

    def _register_signals(self, app):
        """Register signals."""
        before_record_index.dynamic_connect(
            indexer.indexer_receiver,
            sender=app,
            index="records-record-v1.0.0", weak=False)

        file_deleted.connect(update_record_files_async, weak=False)
        file_uploaded.connect(update_record_files_async, weak=False)
