import json

from flask import current_app, make_response
from invenio_records_rest.views import pass_record, need_record_permission
from invenio_rest import ContentNegotiatedMethodView


def make_json_response(data):
    response = current_app.response_class(
        json.dumps(data),
        mimetype='application/json')
    response.status_code = 200

    return response
default = {'GET': {'application/json' : make_json_response}, 'POST':{'application/json' : make_json_response}}
class RecordActionList(ContentNegotiatedMethodView):
    view_name = '{0}_{1}'
    #todo jako velky dir s get a put
    def __init__(self, method, permissions, serializers = default):
        super().__init__(
            method_serializers=serializers,
            default_method_media_type={
                'GET': 'application/json',
                'PUT': 'application/json'
            },
            default_media_type= 'application/json'
        )
        self.method = method
        self.action_permission_factory = permissions


    @need_record_permission('action_permission_factory')
    def get(self, **kwargs):
        method = self.method.get('get')
        return method(**kwargs)

    @need_record_permission('action_permission_factory')
    def put(self, **kwargs):
        return '<h3>male jej</h3>'

