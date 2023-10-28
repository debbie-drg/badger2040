import badger2040
import jpegdec

# Get display width and height
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# Initialize display

display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)

jpeg = jpegdec.JPEG(display.display)


def clear() -> None:
    display.set_pen(0)
    display.clear()


def set_thickness(thickness: int) -> None:
    display.set_thickness(thickness)


def measure_text(text: str, font: str, size: float) -> int:
    display.set_font(font)
    return display.measure_text(text, size)


def draw_rectangle(
    light_value: int, x_coord: int, y_coord: int, width: int, height: int
) -> None:
    display.set_pen(light_value)
    display.rectangle(x_coord, y_coord, width, height)


def draw_display_border(width: int) -> None:
    display.set_pen(15)
    display.rectangle(width, width, WIDTH - 2 * width, HEIGHT - 2 * width)


def draw_empty_rectangle(
    x_coord: int, y_coord: int, width: int, height: int
) -> None:
    display.set_pen(0)
    
    display.line(x_coord, y_coord, x_coord, y_coord + height)
    display.line(x_coord, y_coord, x_coord + width, y_coord)
    display.line(x_coord, y_coord + height, x_coord + width, y_coord + height)
    display.line(x_coord + width, y_coord, x_coord + width, y_coord + height)


def draw_line(
    light_value: int,
    x_coord_start: int,
    y_coord_start: int,
    x_coord_end: int,
    y_cord_end: int,
) -> None:
    display.set_pen(light_value)
    display.line(x_coord_start, y_coord_start, x_coord_end, y_cord_end)


def draw_text(
    text: str,
    font: str,
    light_value: int,
    x_coord: int,
    y_coord: int,
    width: int,
    size: float,
) -> None:
    display.set_pen(light_value)
    display.set_font(font)
    display.text(text, x_coord, y_coord, width, size)


def draw_centered_text(
    text: str,
    font: str,
    light_value: int,
    x_coord: int,
    y_coord: int,
    width: int,
    size: float,
) -> None:
    while True:
        length = display.measure_text(text, size)
        if length >= width and size >= 0.1:
            size -= 0.01
        else:
            break
    display.set_pen(light_value)
    display.set_font(font)
    offset = (width - length) // 2
    display.text(text, x_coord + offset, y_coord, width, size)


def draw_text_fit_width(
    text: str,
    font: str,
    light_value: int,
    x_coord: int,
    y_coord: int,
    width: int,
    size: float,
) -> None:
    while True:
        length = display.measure_text(text, size)
        if length >= width and size >= 0.1:
            size -= 0.01
        else:
            break
    display.set_pen(light_value)
    display.set_font(font)
    display.text(text, x_coord, y_coord, width, size)


def draw_image(image_path: str, x_coord: int, y_coord: int) -> None:
    jpeg.open_file(image_path)
    jpeg.decode(x_coord, y_coord)


def update() -> None:
    display.update()


def partial_update(
    x_coord: int, y_coord: int, width: int, height: int
) -> None:
    display.partial_update(x_coord, y_coord, width, height)


def woken_by_button() -> None:
    return badger2040.woken_by_button()


def led(value: int) -> None:
    display.led(value)


def halt() -> None:
    display.halt()
