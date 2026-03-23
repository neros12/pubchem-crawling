import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

from modules.action import get_pubchem_data


os.makedirs("log", exist_ok=True)


handler = TimedRotatingFileHandler(
    filename="log/crawler.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


if __name__ == "__main__":
    pass
