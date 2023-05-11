from typing import Optional
from src.api import api, request
from src.modules.config import Config
from src.modules.response import Response, JsonResponse


@api.before_request
def auth() -> Optional[Response]:
  """Authentication"""
  config = Config()
  token = config.env('ACCESS_TOKEN')

  if (not token):
    raise Exception("Environment variable 'ACCESS_TOKEN' not found")

  if not 'authorization' in request.headers:
    return JsonResponse.error(401, ["Header 'Authorization' is required"])

  header_token = request.headers['authorization'].strip('Bearer ')

  if (header_token != token):
    return JsonResponse.error(401, ['Unauthorized, this token is invalid'])