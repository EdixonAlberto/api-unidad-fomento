from src.api import api
from src.modules.response import Response, JsonResponse
from src.utils.time_util import Date


@api.get("/status")
def status() -> Response:
  timestamp = Date.get_timestamp()['utc']

  return JsonResponse.ok({
      'api_version': '0.0.1',
      'date_server': timestamp,
      'description': 'API Rest para consultar el valor de la unidad de fomento en Chile',
      'status': 'OK'
  })
