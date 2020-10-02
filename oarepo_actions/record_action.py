import json

from flask import current_app
from invenio_records_rest.views import pass_record, need_record_permission
from invenio_rest import ContentNegotiatedMethodView


def make_json_response(data):
    response = current_app.response_class(
        json.dumps(data),
        mimetype='application/json')
    response.status_code = 200

    return response
default = {'GET': {'application/json' : make_json_response}, 'POST':{'application/json' : make_json_response}}
class RecordAction(ContentNegotiatedMethodView):
    view_name = '{0}_{1}'

    def __init__(self, method, permissions, serializers= default):
        super().__init__(
            method_serializers=serializers,
            default_method_media_type={
                'GET': 'application/json',
                'PUT': 'application/json'
            },
            default_media_type='application/json'
        )
        self.method = method
        self.action_permission_factory = permissions
        #self.serializers = serializers


    @pass_record
    @need_record_permission('action_permission_factory')
    def get(self, pid, record, **kwargs):
        #return getattr(record, self.method)(**kwargs)
        # return self.make_response(
        #     pid, record, links_factory=self.links_factory)
        method = self.method.get('get')
        return getattr(record,method.__name__ )(**kwargs)
