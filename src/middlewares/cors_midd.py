from typing import Optional
from src.api import bp_api, request
from src.modules.config import Config
from src.modules.response import Response, JsonResponse


@bp_api.before_request
def custom_cors() -> Optional[Response]:
  """Custom Cors"""
  config = Config()
  white_list = config.env('WHITE_LIST')

  if (not white_list):
    raise Exception("Environment variable 'WHITE_LIST' not found")

  if not 'origin' in request.headers:  # Ignore requests coming from servers
    return

  origin = request.headers['origin']
  white_list = white_list.split(',')

  if not origin in white_list:
    return JsonResponse.error(401, ['Unauthorized, this origin not allowed'])
