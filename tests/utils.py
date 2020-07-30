import json
from typing import Union


def load_json(path: str) -> Union[list, dict]:
    with open(path) as f:
        return json.load(f)
