# get
import json
from pprint import pprint

def _get_step(value, step: str):
    try:
        return value[step]
    except (AttributeError, TypeError, KeyError):
        return getattr(value, step)

def get(value, path: str):
    try:
        for step in path.split("."):
            value = _get_step(value, step)
        return value
    except (AttributeError, TypeError, KeyError) as e:
        pprint(value)
        raise e

def getOrNone(value, path: str):
    try:
        for step in path.split("."):
            value = _get_step(value, step)
        return value
    except (AttributeError, TypeError, KeyError):
        return None

# log
def log(data):
    with open("log.txt", "w+") as f:
        f.write(json.dumps(data, indent=2))
