import time
import logging
import urllib3
import requests
from typing import Dict, Any


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def http_request(url: str, retry=5):
    for i in range(retry):
        try:
            res = requests.get(url, verify=False, timeout=10)
            res.raise_for_status()
            data: Dict[Any, Any] = res.json()

            return data
        except:
            if i == retry - 1:
                return

            time.sleep(0.5)


def write_log(message: str):
    logging.warning(message)
