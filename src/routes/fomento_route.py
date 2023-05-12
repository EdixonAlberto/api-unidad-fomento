from src.api import api, request,  Resource, fields, create_response_model, response_error_model, parser_auth
from src.modules.response import Response, JsonResponse, OK, BAD_REQUEST, UNAUTHORIZED, NOT_FOUND
from src.modules.scraping import ScrapingSII
from src.utils.time_util import Date

# Create documentation of models
unit_fomento_model = api.model('UnitFomento', {
    'query_date_timestamp': fields.String,
    'unit': fields.Float,
    'unit_string': fields.String
})
response_model = create_response_model('ResponseUnitFomento', unit_fomento_model)


# Craete documentation of params
parser = api.parser()
parser.add_argument('date', type=str, help='Date with format: 01-01-2013', location='params')


@api.route('/unidad_fomento')
class FomentoRoute(Resource):
  @api.doc(description='Unit Fomento')
  @api.expect(parser_auth, parser)
  @api.response(int(OK), description='Unit fomento', model=response_model)
  @api.response(int(BAD_REQUEST), description='Error request', model=response_error_model)
  @api.response(int(NOT_FOUND), description='Not found', model=response_error_model)
  @api.response(int(UNAUTHORIZED), description='Unauthorized', model=response_error_model)
  def get(self) -> Response:
    """Get the value of the Unit Formento for a specific date"""
    query_date = request.args.get('date')

    if (not query_date):
      return JsonResponse.error(BAD_REQUEST, [
          "Query param 'date' is required",
          "Query param 'date' should have this format: 01-01-2013"
      ])

    query_datetime = Date.validate_format_date(query_date)

    if (not query_datetime):
      return JsonResponse.error(BAD_REQUEST, [
          "Query param 'date' should have this format: 01-01-2013"
      ])

    try:
      scraping_sii = ScrapingSII(query_date)
      unit_string = scraping_sii.get_unit_fomento()
      query_date_timestamp = Date.get_timestamp(query_datetime)['utc']

      if (not unit_string):
        raise Exception('not_found')

      unit_format_number: str = unit_string.replace('.', '').replace(',', '.')
      unit: float = float(unit_format_number)

      return JsonResponse.ok({
          'query_date_timestamp': query_date_timestamp,
          'unit': unit,
          'unit_string': unit_string
      })
    except Exception as error:
      if (str(error) == 'not_found'):
        return JsonResponse.not_found('Unit fomento could not be found for this date')
      else:
        raise error
