from typing import Optional
from flask import request
from flask.wrappers import Response
from src.api import api
from src.modules.config import Config
from src.modules.response import JsonResponse


@api.before_request
def custom_cors() -> Optional[Response]:
  """Custom Cors"""
  config = Config()

  if not 'origin' in request.headers:
    return

  origin = request.headers['origin']
  white_list = config.env('WHITE_LIST')

  if (not white_list):
    print('ERROR: Environment variable "WHITE_LIST" not found')
    return JsonResponse.error(500, ['Server error'])

  white_list = white_list.split(',')

  if not origin in white_list:
    return JsonResponse.error(401, ['Unauthorized, this origin not allowed'])
