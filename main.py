import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

from modules import utils
from modules.action import get_pubchem_data


os.makedirs("log", exist_ok=True)


# SET LOGGER #
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


starting_cid = utils.get_checkpoint()
ending_cid = 177929229

l_cid = (starting_cid // 10000) * 10000 + 1
u_cid = l_cid + 9999
for cid in range(starting_cid, ending_cid + 1):
    # ===================================== #
    _start_time = time.time()

    data = get_pubchem_data(cid)
    if data:
        utils.save_data(l_cid, u_cid, data)

    if cid == u_cid:
        utils.update_checkpoint(cid)
        l_cid = cid + 1
        u_cid = l_cid + 9999

    _end_time = time.time()
    # ===================================== #
    _elapsed_time = _end_time - _start_time
    if _elapsed_time < 0.5:
        time.sleep(0.5 - _elapsed_time)
