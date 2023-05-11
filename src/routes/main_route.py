from datetime import datetime
from src.api import api
from src.modules.response import Response, JsonResponse


@api.get("/status")
def status() -> Response:
  timestamp_unix = datetime.utcnow()
  timestamp_utc = timestamp_unix.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

  return JsonResponse.ok({
      'api_version': '0.0.1',
      'date_server': timestamp_utc,
      'description': 'API Rest para consultar el valor de la unidad de fomento en Chile',
      'status': 'OK'
  })
