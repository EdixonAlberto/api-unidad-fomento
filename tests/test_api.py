import unittest
from run import Main


class TestApi(unittest.TestCase):
  def setUp(self):
    self.app = Main().app
    self.app.testing = True
    self.app_test = self.app.test_client()

  def tearDown(self) -> None:
    pass

  def test_ping(self):
    response = self.app_test.get('/api/ping')
    self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
  unittest.main()
