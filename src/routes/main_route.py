from src.api import api, Resource, fields, create_response_model, response_error_model, parser_auth
from src.modules.response import Response, JsonResponse, OK, UNAUTHORIZED
from src.utils.time_util import Date

# Create documentation of models
status_model = api.model('Status', {
    'api_version': fields.String,
    'date_server': fields.String,
    'description': fields.String,
    'status': fields.String
})
response_model = create_response_model('ResponseStatus', status_model)


@api.route("/status")
class MainRoute(Resource):
  @api.doc(description='API Status')
  @api.expect(parser_auth)
  @api.response(int(OK), 'API Status', model=response_model)
  @api.response(int(UNAUTHORIZED), description='Unauthorized', model=response_error_model)
  def get(self) -> Response:
    """Get API status"""
    timestamp = Date.get_timestamp()['utc']

    return JsonResponse.ok({
        'api_version': api.version,
        'date_server': timestamp,
        'description': api.description,
        'status': 'OK'
    })
