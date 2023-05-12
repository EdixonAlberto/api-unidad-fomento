from src.api import bp_api
from src.modules.response import Response, JsonResponse, NOT_FOUND, INTERNAL_SERVER_ERROR


@bp_api.app_errorhandler(NOT_FOUND)
def error_routes(res: Response) -> Response:
  """Handler error of routes"""
  return JsonResponse.not_found('Route not found')


@bp_api.app_errorhandler(INTERNAL_SERVER_ERROR)
def error_server(error) -> Response:
  """Handler error of server flask"""
  return internal_server_error(error)


@bp_api.app_errorhandler(Exception)
def error_python(error) -> Response:
  """Handler error of code python"""
  return internal_server_error(error)


def internal_server_error(error) -> Response:
  print(f"ERROR: {error}")
  return JsonResponse.error(INTERNAL_SERVER_ERROR, ['Server error', str(error)])
