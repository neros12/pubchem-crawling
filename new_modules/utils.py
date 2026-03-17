import time
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


def match_heading(value: str, data_list: list[Dict[str, Any]] | None):
    if data_list:
        for data in data_list:
            target = data.get("TOCHeading", "")
            if target == value:

                return data


def parse_computed_descriptors(name, sections) -> str | None:
    try:
        data = match_heading(name, sections)
        if data:
            return data["Information"][0]["Value"]["StringWithMarkup"][0]["String"]
    except:
        pass
