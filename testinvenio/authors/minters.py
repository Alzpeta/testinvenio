# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 CERN.
# Copyright (C) 2018 RERO.
#
# Invenio-Circulation is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Circulation minters."""

from .providers import AuthorIdProvider
from invenio_oaiserver.provider import OAIIDProvider

from datetime import datetime

from flask import current_app
from invenio_pidstore import current_pidstore
from invenio_oaiserver.utils import datetime_to_datestamp

def author_pid_minter(record_uuid, data):
    """Mint loan identifiers."""
    assert 'id' not in data
    provider = AuthorIdProvider.create(
        object_type='rec',
        object_uuid=record_uuid,
    )
    data['id'] = provider.pid.pid_value
    return provider.pid

# def oai_pid_minter(record_uuid, data):
#     pid_value = data.get('_oai', {}).get('id')
#     if pid_value is None:
#         fetcher_name = \
#             current_app.config.get('OAISERVER_CONTROL_NUMBER_FETCHER', 'recid')
#         cn_pid = current_pidstore.fetchers[fetcher_name](record_uuid, data)
#         pid_value = current_app.config.get('OAISERVER_ID_PREFIX', '') + str(
#             cn_pid.pid_value
#         )
#     provider = OAIIDProvider.create(
#         object_type='rec', object_uuid=record_uuid,
#         pid_value=str(pid_value)
#     )
#     data.setdefault('_oai', {})
#     data['_oai']['id'] = provider.pid.pid_value
#     return provider.pid
