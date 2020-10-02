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

    #app.config['OAISERVER_RECORD_INDEX'] = 'marc21',
    app.config['OAISERVER_ID_PREFIX'] = 'oai:example:',
    # app.config['OAISERVER_METADATA_FORMATS'] = {'oai_dc':{
    #         'serializer': (
    #             'invenio_oaiserver.utils:dumps_etree', {
    #                 'xslt_filename': pkg_resources.resource_filename(
    #                     'testinvenio.records', 'static/xsl/MARC21slim2OAIDC.xsl'
    #                 ),
    #                 #'xslt_filename': pathlib.Path("home/alzbeta/testinvenio/records/static/xsl/MARC21slim2OAIDC.xsl").absolute()
    #             }
    #         ),
    #         'schema': 'http://json-schema.org/draft-04/schema#',
    #         'namespace': 'http://json-schema.org/draft-04/schema#',
    #     }}

    ext_oaiserver = InvenioOAIServer(app)
    app.register_blueprint(blueprint)
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    ext_search.flush_and_refresh('_all')
    oaiset = OAISet(spec='title5', name='Title5', description='...')
    #nefunguje pokud search pattern ma pole ktere neni v obouch modelech...
    #oaiset.search_pattern = 'title:S'
    try:
        print("1")
        db.session.add(oaiset)
        db.session.commit()
    except:
        pass
    # with app.test_client() as client:
    #     response = client.get('/api/records/')
    #     #response = client.post('/api/records/', data=json.dumps({"title": "neco", "contributors": [{"name": "nekdo"}], "owner": 1}), content_type='application/json')
    # print(response.data)
    # with app.test_client() as client:
    #     res = client.get('https://127.0.0.1:5000/oai2d?verb=ListSets')
    # print(res.data)
    #print(b'Title' in res.data)


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
        #app_loaded.connect(oai_server)
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