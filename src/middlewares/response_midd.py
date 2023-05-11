from src.modules.response import Response
from src.api import api


@api.after_request
def add_headers(res: Response) -> Response:
  res.headers['Content-Type'] = 'application/json'
  res.headers['X-Frame-Options'] = 'SAMEORIGIN'
  res.headers['X-XSS-Protection'] = '1; mode=block'
  res.headers['X-Content-Type-Options'] = 'nosniff'
  return res
