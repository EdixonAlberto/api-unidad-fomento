from src.api import api
from src.modules.response import Response, JsonResponse


@api.get('/ping')
def ping() -> Response:
  return JsonResponse.ok('pong')
