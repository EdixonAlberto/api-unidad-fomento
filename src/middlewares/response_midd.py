from src.api import bp_api
from src.modules.response import Response


@bp_api.after_request
def add_headers(res: Response) -> Response:
  res.headers['X-Frame-Options'] = 'SAMEORIGIN'
  res.headers['X-XSS-Protection'] = '1; mode=block'
  res.headers['X-Content-Type-Options'] = 'nosniff'
  return res
