from src.api import api, request
from src.modules.response import Response, JsonResponse
from src.modules.scraping import ScrapingSII
from src.utils.time_util import Date


@api.get('/unidad_fomento')
def unidad_fomento() -> Response:
  query_date = request.args.get('date')

  if (not query_date):
    return JsonResponse.error(400, [
        "Query param 'date' is required",
        "Query param 'date' should have this format: 01-01-2013"
    ])

  query_datetime = Date.validate_format_date(query_date)

  if (not query_datetime):
    return JsonResponse.error(400, [
        "Query param 'date' should have this format: 01-01-2013"
    ])

  try:
    scraping_sii = ScrapingSII(query_date)
    unit_string = scraping_sii.get_unit_fomento()
    query_date_timestamp = Date.get_timestamp(query_datetime)['utc']

    if (not unit_string):
      raise Exception('not_found')

    unit_format_float: str = unit_string.replace('.', '').replace(',', '.')
    unit: float = float(unit_format_float)

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
