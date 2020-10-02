import invenio_base
from flask import url_for, abort, Blueprint
from invenio_app.helpers import obj_or_import_string
from invenio_base.signals import app_loaded
import inspect

from invenio_records_rest.utils import allow_all

from .record_action import RecordAction
from .record_action_list import RecordActionList


def action_urls(sender, app=None, **kwargs):
    actions = Blueprint("oarepo_actions", __name__, url_prefix=None, )
    meths = []
    rest_endpoints = app.config["RECORDS_REST_ENDPOINTS"]
    for endpoint, configuration in rest_endpoints.items():

        if 'record_class' not in configuration:
            continue
        record_class = configuration['record_class']
        record_class = obj_or_import_string(record_class)
        for name, function in inspect.getmembers(record_class):
            if hasattr(function, '__action'):
                attribut_content = getattr(function, '__action')
                if 'meth' in attribut_content and 'url_path' in attribut_content and attribut_content[
                    'meth'] not in meths:
                    meths.append(attribut_content['url_path'])
        for name, function in inspect.getmembers(record_class):
            if hasattr(function, '__action'):
                attribut_content = getattr(function, '__action')
                if 'url_path' in attribut_content and attribut_content['url_path'] not in meths:
                    if 'meth' not in attribut_content:
                        method = {'get': function}
                    else:
                        method = {attribut_content['meth']: function}
                elif 'meth' not in attribut_content:
                    method = {'get': function}
                elif 'url_path' in attribut_content and attribut_content['url_path'] in meths:
                    pass
                else:
                    method = {attribut_content['meth']: function}
                try:
                    permissions = attribut_content['permissions']
                except:
                    permissions = allow_all
                try:
                    serializers = attribut_content[serializers]
                except:
                    serializers = None
                if 'detail' in attribut_content:
                    if 'url_path' in attribut_content:
                        route_rule = configuration['list_route'] + attribut_content['url_path']
                    else:
                        route_rule = configuration['list_route'] + name
                    if serializers != None:
                        actions.add_url_rule(route_rule,
                                         view_func=RecordActionList.as_view(
                                             RecordActionList.view_name.format(endpoint, name), method=method,
                                             permissions=permissions, serializers=serializers))
                    else:
                        actions.add_url_rule(route_rule,
                                             view_func=RecordActionList.as_view(
                                                 RecordActionList.view_name.format(endpoint, name), method=method,
                                                 permissions=permissions))
                else:
                    if 'url_path' in attribut_content:
                        if attribut_content['url_path'][1] != '/':
                            route_rule = configuration['item_route'] + '/' + attribut_content['url_path']
                        else:
                            route_rule = configuration['item_route'] + attribut_content['url_path']
                    else:
                        route_rule = configuration['item_route'] + '/' + name
                    if serializers != None:
                        actions.add_url_rule(route_rule,
                                         view_func=RecordAction.as_view(RecordAction.view_name.format(endpoint, name),
                                                                        method=method,
                                                                        permissions=permissions,
                                                                        serializers=serializers))
                    else:
                        actions.add_url_rule(route_rule,
                                             view_func=RecordAction.as_view(
                                                 RecordAction.view_name.format(endpoint, name),
                                                 method=method,
                                                 permissions=permissions))
    app.register_blueprint(actions)


def function(sender, app=None, **kwargs):
    actions = Blueprint("oarepo_actions", __name__, url_prefix=None, )
    rest_endpoints = app.config["RECORDS_REST_ENDPOINTS"]
    print(list(sorted(rest_endpoints.keys())))
    for endpoint, configuration in rest_endpoints.items():
        if 'record_class' not in configuration:
            continue
        record_class = configuration['record_class']
        record_class = obj_or_import_string(record_class)
        for f in inspect.getmembers(record_class):
            name, function = f
            if hasattr(function, '__action'):
                attribut_content = getattr(function, '__action')
                method = list()
                method.append(function)
                if ('meth' in attribut_content):
                    method.append(attribut_content['meth'])
                else:
                    method.append('get')
                if 'detail' in attribut_content:
                    if 'url_path' in attribut_content:
                        route_rule = configuration['list_route'] + attribut_content['url_path']
                    else:
                        route_rule = configuration['list_route'] + name
                    actions.add_url_rule(route_rule,
                                         view_func=RecordActionList.as_view(
                                             RecordActionList.view_name.format(endpoint, name),
                                             method=method, permissions=attribut_content['permissions'],
                                             serializers=attribut_content['serializers']))
                else:
                    if 'url_path' in attribut_content:

                        if attribut_content['url_path'][1] != '/':
                            route_rule = configuration['item_route'] + '/' + attribut_content['url_path']
                        else:
                            route_rule = configuration['item_route'] + attribut_content['url_path']
                    else:
                        route_rule = configuration['item_route'] + '/' + name
                        # todo je povoleny tam to permission nemit? + osetrit
                    actions.add_url_rule(route_rule,
                                         view_func=RecordAction.as_view(RecordAction.view_name.format(endpoint, name),
                                                                        method=name,
                                                                        permissions=attribut_content['permissions']))
    app.register_blueprint(actions)
    print(app.url_map)


class Actions(object):
    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""

        app.extensions['testinvenio-oarepo_actions'] = self
        app_loaded.connect(action_urls)
