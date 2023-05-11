from flask import Flask
from src.modules.config import Config
from src.api import api
from src.routes import main_route, fomento_route
from src.middlewares import (
    cors_midd,
    response_midd,
    errors_midd,
    auth_midd
)


class Server(Config):
  app: Flask

  def __init__(self) -> None:
    super().__init__()
    self.app = Flask(__name__)
    self.routes_middlewares()

  def routes_middlewares(self) -> None:
    self.app.register_blueprint(api)

  def start(self) -> None:
    port = self.env('PORT')
    port = int(port) if port is not None else 3000

    mode_dev = self.env('MODE_API') == 'development'
    debug = True if mode_dev else False

    self.app.run(debug=debug, port=port, use_reloader=True)
