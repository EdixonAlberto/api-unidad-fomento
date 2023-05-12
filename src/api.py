from flask import Blueprint, request
from flask_restx import Api, Resource, fields

bp_api = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    bp_api,
    doc='/doc/',
    version='1.0.0',
    title='API Unidad Fomento',
    description='API Rest para consultar el valor de la unidad de fomento en Chile',
    license='License MIT',
    license_url='https://github.com/EdixonAlberto/api-unidad-fomento/blob/main/LICENSE',
    default='Endpoints',
    default_label='',
    security=['access_token'],
    authorizations={
        'access_token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
)

parser_auth = api.parser()
parser_auth.add_argument('Authorization', type=str, help='Access token', location='headers')

response_error_model = api.model('ResponseError', {
    'errors': fields.List(fields.String),
    'response': fields.String,
    'status_code': fields.Integer
})


def create_response_model(name: str, model):
  return api.model(name, {
      'errors': fields.List(fields.String),
      'response': fields.Nested(model),
      'status_code': fields.Integer
  })
