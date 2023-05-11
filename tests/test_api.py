import pytest
from src.modules.server import Server


@pytest.fixture()
def app():
  app = Server().app
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


def test_status(client):
  response = client.get("/api/status")
  data = response.json
  status = data['response']['status']
  assert status == 'OK'


def test_unidad_fomento(client):
  response = client.get("/api/unidad_fomento?date=01-01-2013")
  data = response.json
  unit = data['response']['unit']
  assert float(unit) == 22837.06
