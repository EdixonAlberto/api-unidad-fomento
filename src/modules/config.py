from typing import Optional, Dict
from os import getenv
from dotenv import load_dotenv, dotenv_values


class Config():
  _env: Dict[str, Optional[str]]

  def __init__(self) -> None:
    load_dotenv()
    self._env = dotenv_values('.env')

  def env(self, name) -> Optional[str]:
    mode_dev = self._env.get('MODE_API') == 'development'
    return self._env.get(name) if mode_dev else getenv(name)
