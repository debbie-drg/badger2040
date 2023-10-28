import os
import qrcode
import display

from global_constants import QR_CODE_DIRECTORY

WIDTH, HEIGHT = display.WIDTH, display.HEIGHT
QR_WIDTH = 128

code = qrcode.QRCode()

# ------------------------------
#        QR Code Functions
# ------------------------------


def measure_qr_code(size: int, code: qrcode) -> tuple(int, int):
    width, _ = code.get_size()
    module_size = int(size / width)
    return module_size * width, module_size


def draw_qr_code(ox, oy, size, code) -> None:
    size, module_size = measure_qr_code(size, code)
    display.draw_rectangle(15, ox, oy, size, size)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.draw_rectangle(
                    0,
                    ox + x * module_size,
                    oy + y * module_size,
                    module_size,
                    module_size,
                )


def draw_qr_file(index: int = 0, skew: str = "normal") -> None:
    try:
        CODES = [
            f for f in os.listdir(f"/{QR_CODE_DIRECTORY}/{skew}") if f.endswith(".txt")
        ]
    except OSError:
        print(f"No QR codes found for skew {skew}")
        return

    if len(CODES) == 0:
        print(f"No QR codes in skew {skew}. Code will not be printed.")
        return

    index = index % len(CODES)
    file = CODES[index]
    TOTAL_CODES = len(CODES)

    codetext = open(f"{QR_CODE_DIRECTORY}/{skew}/{file}", "r")
    lines = codetext.read().strip().split("\n")
    codetext.close()

    code_text = lines.pop(0)
    title_text = lines.pop(0)
    detail_text = lines

    # Clear the Display and draw border
    display.draw_display_border(1)
    display.draw_line(0, QR_WIDTH, 0, QR_WIDTH, HEIGHT - 1)

    # Get code and size
    code.set_text(code_text)
    size, _ = measure_qr_code(QR_WIDTH, code)
    left = top = int((HEIGHT / 2) - (size / 2))
    draw_qr_code(left, top, 128, code)
    left = QR_WIDTH + 5

    # Draw black box around name and print name
    display.draw_rectangle(0, QR_WIDTH, 0, WIDTH - QR_WIDTH, 26)
    display.draw_centered_text(
        title_text, "bitmap6", 15, QR_WIDTH, 2, WIDTH - QR_WIDTH, 3
    )

    # Draw detail lines

    top = 32
    for line in detail_text:
        display.draw_text(line, "bitmap14_outline", 0, left, top, WIDTH - QR_WIDTH, 0.4)
        top += 13

    # Draw box around bottom
    display.draw_rectangle(0, QR_WIDTH, HEIGHT - 26, WIDTH - QR_WIDTH, 26)

    # Draw bottom text
    display.draw_text(
        "Scan the code!", "bitmap6", 15, left, HEIGHT - 19, WIDTH - QR_WIDTH, 2
    )

    # Draw squares to indicate QR number if more than one

    if TOTAL_CODES > 1:  # This would draw squares hinting to the number of QR codes
        for i in range(TOTAL_CODES):
            x = 286
            y = int((128 / 2) - (TOTAL_CODES * 10 / 2) + (i * 10))
            display.draw_rectangle(0, x, y, 8, 8)
            if index != i:
                display.draw_rectangle(15, x + 1, y + 1, 6, 6)

    display.update()


# Main programme for testing purposes
if __name__ == "__main__":
    draw_qr_file()
