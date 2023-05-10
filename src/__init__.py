from src.modules.server import Server


class Main(Server):
  def __init__(self) -> None:
    super().__init__()
    self.start()
