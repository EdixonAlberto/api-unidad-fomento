from typing import List, Union
from flask import jsonify, make_response
from flask.wrappers import Response


class JsonResponse():
  @staticmethod
  def ok(response: Union[dict, str, int, float]) -> Response:
    res = make_response(jsonify(
        status_code=200,
        response=response,
        errors=[]
    ))
    res.status_code = 200
    return res

  @staticmethod
  def error(status: int, errors: Union[List[str], None] = []) -> Response:
    res = make_response(jsonify(
        status_code=status,
        response=None,
        errors=errors
    ))
    res.status_code = status
    return res
