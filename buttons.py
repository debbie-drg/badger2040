import machine

buttons = {
    "a": 12,
    "b": 13,
    "c": 14,
    "up": 15,
    "down": 11,
}


def is_pressed(button: str) -> int:
    try:
        return machine.Pin(buttons[button]).value()
    except KeyError:
        print("Invalid button")
        return 0
