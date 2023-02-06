import os
import json


def state_defaults():
    state = {
        "mode": "badge",
        "skew": "normal",
        "index": 0,
        "skew_index": 0,
        "gallery_index": 0,
    }
    return state


def state_load(app, state) -> bool:
    try:
        data = json.loads(open("/state/{}.json".format(app), "r").read())
        if type(data) is dict:
            state.update(data)
            return True
    except (OSError, ValueError):
        pass

    return False


def state_delete(app) -> None:
    try:
        os.remove("/state/{}.json".format(app))
    except OSError:
        pass


def state_save(app, data) -> None:
    try:
        with open("/state/{}.json".format(app), "w") as f:
            f.write(json.dumps(data))
            f.flush()
    except OSError:
        try:
            os.stat("/state")
        except OSError:
            os.mkdir("/state")
            state_save(app, data)


def state_modify(app, data) -> None:
    state = {}
    state_load(app, state)
    state.update(data)
    state_save(app, state)
