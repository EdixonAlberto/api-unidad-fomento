from src.api import api, request,  Resource, fields, create_response_model, response_error_model, parser_auth
from src.modules.response import Response, JsonResponse, OK, BAD_REQUEST, UNAUTHORIZED, NOT_FOUND
from src.modules.scraping import ScrapingSII, UnitFomentoDict, Optional
from src.utils.time_util import Date

# Create documentation of models
unit_model = api.model('Unit', {
    'unit': fields.Float,
    'unit_string': fields.String
})
unit_fomento_model = unit_model.inherit('Unit', {
    'query_date_timestamp': fields.String,
})
unit_fomento_list_model = api.model('UnitFomentoList', {
    'month_key': fields.Nested(api.model('Month', {
        'day_key': fields.Nested(unit_model)
    }))
})
response_model = create_response_model('ResponseUnitFomento', unit_fomento_model)
response_list_model = create_response_model('ResponseUnitFomentoList', unit_fomento_list_model)

# Craete documentation of params
parser = api.parser()
parser.add_argument('date', type=str, help='Date with format: 01-01-2013', location='params')

parserList = api.parser()
parserList.add_argument('year', type=str, help='Year with format: 2013', location='params')


@api.route('/unidad_fomento')
@api.response(int(BAD_REQUEST), description='Error request', model=response_error_model)
@api.response(int(NOT_FOUND), description='Not found', model=response_error_model)
@api.response(int(UNAUTHORIZED), description='Unauthorized', model=response_error_model)
class FomentoRoute(Resource):
  @api.doc(description='Unit Fomento')
  @api.expect(parser_auth, parser)
  @api.response(int(OK), description='Unit fomento', model=response_model)
  def get(self) -> Response:
    """Get the value of the Unit Fomento for a specific date"""
    query_date = request.args.get('date')

    if (not query_date):
      return JsonResponse.error(BAD_REQUEST, [
          "Query param 'date' is required",
          "Query param 'date' should have format of date: 01-01-2013"
      ])

    query_datetime = Date.validate_format_date(query_date)

    if (not query_datetime):
      return JsonResponse.error(BAD_REQUEST, [
          "Query param 'date' should have format of date: 01-01-2013"
      ])

    # Validate minimun date that can be consulted
    MINUMUN_DATE: str = '01-01-2013'
    minimum_datetime = Date.validate_format_date(MINUMUN_DATE)
    minimum_timestamp: float = minimum_datetime.timestamp() if (minimum_datetime != None) else 0
    query_timestamp: float = query_datetime.timestamp() if (query_datetime != None) else 0

    if (query_timestamp < minimum_timestamp):
      return JsonResponse.error(BAD_REQUEST, [
          f"The minimum date that can be consulted is: {MINUMUN_DATE}"
      ])

    try:
      scraping_sii = ScrapingSII(query_date)
      unit_fomento: Optional[UnitFomentoDict] = scraping_sii.get_unit_fomento()

      if (not unit_fomento):
        raise Exception('not_found')

      query_date_timestamp = Date.get_timestamp_utc(query_datetime)
      return JsonResponse.ok({
          'query_date_timestamp': query_date_timestamp,
          **unit_fomento
      })
    except Exception as error:
      if (str(error) == 'not_found'):
        return JsonResponse.not_found('Unit fomento not found for this date')
      else:
        raise error


@api.route('/unidad_fomento_meses')
@api.response(int(BAD_REQUEST), description='Error request', model=response_error_model)
@api.response(int(NOT_FOUND), description='Not found', model=response_error_model)
@api.response(int(UNAUTHORIZED), description='Unauthorized', model=response_error_model)
class FomentoListRoute(Resource):
  @api.doc(description='Months Unit Fomento')
  @api.expect(parser_auth, parserList)
  @api.response(int(OK), description='Months Unit fomento', model=response_list_model)
  def get(self):
    """Get list of months with the values of the Unit Fomento for a specific year"""
    query_year = request.args.get('year')

    if (not query_year):
      return JsonResponse.error(BAD_REQUEST, [
          "Query param 'year' is required",
          "Query param 'year' should have format of year: 2013"
      ])

    query_date: str = f"01-01-{query_year}"
    query_datetime = Date.validate_format_date(query_date)

    if (not query_datetime):
      return JsonResponse.error(BAD_REQUEST, [
          "Query param 'year' should have format of year: 2013"
      ])

    if (int(query_year) < 2013):
      return JsonResponse.error(BAD_REQUEST, [
          f"The minimum year that can be consulted is: 2013"
      ])

    try:
      scraping_sii = ScrapingSII(query_date)
      months_unit_fomento = scraping_sii.get_unit_fomento_list()

      return JsonResponse.ok(months_unit_fomento)
    except Exception as error:
      if (str(error) == 'not_found'):
        return JsonResponse.not_found('Months unit fomento not found for this year')
      else:
        raise error
