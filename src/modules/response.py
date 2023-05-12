from http.client import OK, BAD_REQUEST, UNAUTHORIZED, NOT_FOUND, INTERNAL_SERVER_ERROR
from typing import List, Union
from flask import jsonify, make_response
from flask.wrappers import Response


class JsonResponse():
  @staticmethod
  def ok(response: Union[dict, str, int, float, list]) -> Response:
    res = make_response(jsonify(
        status_code=OK,
        response=response,
        errors=[]
    ))
    res.status_code = OK
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

  @staticmethod
  def not_found(response: str) -> Response:
    res = make_response(jsonify(
        status_code=NOT_FOUND,
        response=response,
        errors=[]
    ))
    res.status_code = NOT_FOUND
    return res
