import os
import json


def state_defaults() -> dict:
    state = {
        "mode": "badge",
        "skew": "normal",
        "index": 0,
        "skew_index": 0,
        "gallery_index": 0,
    }
    return state


def state_load(app: str, state: dict) -> bool:
    try:
        data = json.loads(open(f"/state/{app}.json", "r").read())
        if type(data) is dict:
            state.update(data)
            return True
    except (OSError, ValueError):
        pass

    return False


def state_delete(app: str) -> None:
    try:
        os.remove(f"/state/{app}.json")
    except OSError:
        pass


def state_save(app: str, data: dict) -> None:
    try:
        with open(f"/state/{app}.json", "w") as f:
            f.write(json.dumps(data))
            f.flush()
    except OSError:
        import os

        try:
            os.stat("/state")
        except OSError:
            os.mkdir("/state")
            state_save(app, data)


def state_modify(app, data):
    state = {}
    state_load(app, state)
    state.update(data)
    state_save(app, state)
