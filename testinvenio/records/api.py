# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 alzp.
#
# testInvenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records API."""

from __future__ import absolute_import, print_function

from flask import make_response, abort
from invenio_records_files.api import Record as FilesRecord
from oarepo_actions.decorators import action
from invenio_access.permissions import Permission, authenticated_user, any_user
from flask_principal import Need, RoleNeed
from werkzeug.wrappers import Response


def can():
    return True
class FakeNeed():
    def __init__(self):
        self.method = None
    def can(self):
        return True
class OwnerNeed():
    def __init__(self, record):
        self.record = record

    def can(self, record):
        if record['Owner'] == 1:
            return True
        else:
            return False

def pf(record = None):
    #return Permission(RoleNeed('admin'))
    #return Permission(FakeNeed())
    #return Permission(OwnerNeed(record["owner"]))
    return Permission(any_user)
class Record(FilesRecord):
    """Custom record."""
    # @action(url_path = "blah", permissions = pf)
    # def send_email(self, **kwargs):
    #     return { "title": self["title"]}
    #
    # @classmethod
    # @action(detail=False, url_path = "jej", permissions = pf, serializers = {'GET':{'text/html': make_response},'POST':{'text/html': make_response}})
    # def blah1(cls, **kwargs):
    #     return '<jej>xx</jej>'
    #
    # @classmethod
    # @action(detail=False, url_path="test/<int:param>", permissions=pf, serializers = {'GET':{'text/html': make_response}})
    # def test1(cls, param = None, **kwargs):
    #     print("juch")
    #     return {param: "jej"}
    #
    #
    # # @classmethod
    # # @action(detail=False, url_path="a", permissions=pf, serializers = {'text/html': make_response}, meth = "PUT")
    # # def a(cls, param = None, **kwargs):
    # #     return "<h1>jej</h1>"
    #
    # @classmethod
    # @action(detail=False, permissions=pf, serializers={'text/html': make_response})
    # def test(cls, **kwargs):
    #     print("jej")
    #     return Response(status=200)


    _schema = "records/record-v1.0.0.json"

