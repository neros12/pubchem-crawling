import json
from pathlib import Path
from datetime import datetime, timezone
from typing import TypedDict


class CheckPointDTO(TypedDict):
    last_cid: int
    updated_at: str


BASE_PATH = Path(__file__).parents[1]
CHECKPOINT_PATH = BASE_PATH / "checkpoint.json"


def update_checkpoint(cid: int):
    data: CheckPointDTO = {
        "last_cid": cid,
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    with open(CHECKPOINT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_checkpoint() -> int:
    if not CHECKPOINT_PATH.exists():
        return 0

    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f:
        data: CheckPointDTO = json.load(f)

    return data.get("last_cid", 0)
