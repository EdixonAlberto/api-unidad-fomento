import pytest
from src.modules.server import Server
from src.modules.response import OK, BAD_REQUEST, NOT_FOUND


@pytest.fixture()
def server():
  server = Server()
  return server


@pytest.fixture()
def app(server):
  app = server.app
  app.config.update({
      "TESTING": True,
  })

  # other setup can go here
  yield app
  # clean up / reset resources here


@pytest.fixture()
def client(app):
  return app.test_client()


@pytest.fixture()
def runner(app):
  return app.test_cli_runner()


@pytest.fixture()
def headers(server):
  env = server.env
  origin = env('WHITE_LIST')
  token = env('ACCESS_TOKEN')
  return {
      'Origin': origin,
      'Authorization': token
  }


def test_not_found(client, headers):
  response = client.get("/api/not_found", headers=headers)
  data = response.json
  message = data['response']
  status_code = data['status_code']
  assert message == 'Route not found' and status_code == NOT_FOUND


def test_status(client, headers):
  response = client.get("/api/status", headers=headers)
  data = response.json
  status = data['response']['status']
  assert status == 'OK'


def test_unidad_fomento_ok(client, headers):
  response = client.get("/api/unidad_fomento?date=01-01-2013", headers=headers)
  data = response.json
  status_code = data['status_code']
  unit = data['response']['unit']
  assert status_code == OK and float(unit) == 22837.06


def test_unidad_fomento_error_format(client, headers):
  response = client.get("/api/unidad_fomento?date=01/01/2013", headers=headers)
  data = response.json
  status_code = data['status_code']
  errors = data['errors']
  assert status_code == BAD_REQUEST and errors[0] == "Query param 'date' should have format of date: 01-01-2013"


def test_unidad_fomento_error_minimun_date(client, headers):
  response = client.get("/api/unidad_fomento?date=31-12-2012", headers=headers)
  data = response.json
  status_code = data['status_code']
  errors = data['errors']
  assert status_code == BAD_REQUEST and errors[0] == "The minimum date that can be consulted is: 01-01-2013"


def test_unidad_fomento_not_found(client, headers):
  response = client.get("/api/unidad_fomento?date=01-01-2030", headers=headers)
  data = response.json
  status_code = data['status_code']
  message = data['response']
  assert status_code == NOT_FOUND and (not not message)


def test_unidad_fomento_meses(client, headers):
  response = client.get("/api/unidad_fomento_meses?year=2013", headers=headers)
  data = response.json
  status_code = data['status_code']
  months_list = data['response']
  assert status_code == OK and months_list['january']['31']['unit_string'] == '22.807,54'
