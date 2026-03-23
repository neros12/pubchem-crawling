import time
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, TypedDict

import urllib3
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CheckPointDTO(TypedDict):
    last_cid: int
    updated_at: str


BASE_PATH = Path(__file__).parents[1]
CHECKPOINT_PATH = BASE_PATH / "checkpoint.json"
DATA_PATH = BASE_PATH / "data"


def update_checkpoint(cid: int):
    data: CheckPointDTO = {
        "last_cid": cid,
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_checkpoint() -> int:
    if not CHECKPOINT_PATH.exists():
        return 1

    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
        data: CheckPointDTO = json.load(f)

    return data.get("last_cid", 1)


def save_data(l_cid, u_cid, data):
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    file_path = DATA_PATH / f"{l_cid}-{u_cid}.jsonl"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


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
