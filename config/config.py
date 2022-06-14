import logging
from pathlib import Path

from aiomisc.log import basic_config
from pydantic import BaseSettings, Field

logging_format = (
    '%(filename)s %(funcName)s [LINE:%(lineno)d]# '
    '%(levelname)-8s [%(asctime)s] %(name)s: %(message)s'
)

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigData(BaseSettings):
    DATABASE_ENGINE: str = Field('sqlite:///data.db', env='DATABASE_ENGINE')
    DATABASE_NAME: str = Field('data.db', env='DATABASE_NAME')
    debug: bool = Field(True, env='DEBUG')

    class Config:
        env_file: Path = BASE_DIR / '.env'


cfg = ConfigData()

basic_config(
    format=logging_format,
    level=logging.DEBUG if cfg.debug else logging.INFO,
    filename='app.log',
    buffered=True,
)
