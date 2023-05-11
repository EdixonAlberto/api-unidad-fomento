import pytest
from src.modules.server import Server


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


def test_status(client, headers):
  response = client.get("/api/status", headers=headers)
  data = response.json
  status = data['response']['status']
  assert status == 'OK'


def test_unidad_fomento(client, headers):
  response = client.get("/api/unidad_fomento?date=01-01-2013", headers=headers)
  data = response.json
  unit = data['response']['unit']
  assert float(unit) == 22837.06
