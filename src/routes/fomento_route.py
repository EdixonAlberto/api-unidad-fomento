from datetime import datetime
from src.api import api, request
from src.modules.response import Response, JsonResponse
from src.modules.scraping import ScrapingSII


@api.get('/unidad_fomento')
def unidad_fomento() -> Response:
  query_date = request.args.get('date')

  if (not query_date):
    return JsonResponse.error(400, [
        "Endpoint necesita un query params 'date'"
    ])

  try:
    datetime.strptime(query_date, '%d-%m-%Y')
  except:
    return JsonResponse.error(400, [
        "Query param 'date' debe tener este formato: 01-01-2013"
    ])

  try:
    scraping_sii = ScrapingSII(query_date)
    unit_string = scraping_sii.get_unit_fomento()

    if (not unit_string):
      raise Exception('not_found')

    unit_format_float: str = unit_string.replace('.', '').replace(',', '.')
    unit: float = float(unit_format_float)

    return JsonResponse.ok({
        'unit': unit,
        'unit_string': unit_string,
        'query_date': query_date
    })
  except Exception as error:
    if (str(error) == 'not_found'):
      return JsonResponse.not_found('No se ha podido encontrar unidad de fomento para esta fecha')
    else:
      raise error
