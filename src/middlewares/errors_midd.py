from src.api import api
from src.modules.response import Response, JsonResponse


@api.app_errorhandler(404)
def error_routes(res: Response) -> Response:
  """Handler error of routes"""
  return JsonResponse.not_found('Route not found')


@api.app_errorhandler(500)
def error_server(error) -> Response:
  """Handler error of server flask"""
  return internal_server_error(error)


@api.app_errorhandler(Exception)
def error_python(error) -> Response:
  """Handler error of code python"""
  return internal_server_error(error)


def internal_server_error(error) -> Response:
  print(f"ERROR: {error}")
  return JsonResponse.error(500, ['Server error', str(error)])
