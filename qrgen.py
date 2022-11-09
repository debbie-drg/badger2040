import os
import qrcode
import badger2040

from global_constants import SKEW_LIST, QR_CODE_DIRECTORY, WIDTH, HEIGHT

TOTAL_CODES = dict()
CODES = dict()
# Load all available QR Code Files for each skew
for skew in SKEW_LIST:
    try:
        CODES[skew] = [
            f for f in os.listdir(f"/{QR_CODE_DIRECTORY}/{skew}") if f.endswith(".txt")
        ]
        TOTAL_CODES[skew] = len(CODES[skew])
    except OSError:
        print(f"No QR codes found for skew {skew}")
        pass

code = qrcode.QRCode()

display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# ------------------------------
#        QR Code Functions
# ------------------------------


def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.pen(15)
    display.rectangle(ox, oy, size, size)
    display.pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(
                    ox + x * module_size, oy + y * module_size, module_size, module_size
                )


def draw_qr_file(index: int = 0, skew: str = "normal"):
    display.led(128)

    if TOTAL_CODES[skew] == 0:
        print(f"No QR codes in skew {skew}. Code will not be printed.")
        return None

    index = index % TOTAL_CODES[skew]
    file = CODES[skew][index]
    codetext = open(f"{QR_CODE_DIRECTORY}/{skew}/{file}", "r")

    lines = codetext.read().strip().split("\n")
    code_text = lines.pop(0)
    title_text = lines.pop(0)
    detail_text = lines

    # Clear the Display
    display.pen(15)  # Change this to 0 if a white background is used
    display.clear()
    display.pen(0)

    code.set_text(code_text)
    size, _ = measure_qr_code(128, code)
    left = top = int((badger2040.HEIGHT / 2) - (size / 2))
    draw_qr_code(left, top, 128, code)
    left = 128 + 5

    # Draw a border around the screen and code
    display.pen(0)
    display.thickness(1)
    display.line(0, 0, WIDTH - 1, 0)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)
    display.line(0, 0, 0, HEIGHT - 1)
    display.line(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(128, 0, 128, HEIGHT - 1)

    # Draw black box around name
    display.thickness(26)
    display.line(128 + 13, 13, WIDTH - 1, 13)

    # Draw the header
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("bitmap6")
    display.thickness(1)
    display.text(title_text, left, 3, 3)

    # Draw detail lines
    display.thickness(1)
    display.pen(0)
    display.font("bitmap14_outline")

    top = 32
    for line in detail_text:
        display.text(line, left, top, 0.4)
        top += 13

    # Draw box around bottom line
    display.thickness(26)
    display.line(128 + 13, HEIGHT - 11, WIDTH - 1, HEIGHT - 11)

    # Draw text for last details line
    display.font("bitmap6")
    display.thickness(1)
    display.pen(15)
    display.text("Scan the code!", left, HEIGHT - 19, 2)

    if (
        TOTAL_CODES[skew] > 1
    ):  # This would draw squares hinting to the number of QR codes
        for i in range(TOTAL_CODES[skew]):
            x = 286
            y = int((128 / 2) - (TOTAL_CODES[skew] * 10 / 2) + (i * 10))
            display.pen(0)
            display.rectangle(x, y, 8, 8)
            if index != i:
                display.pen(15)
                display.rectangle(x + 1, y + 1, 6, 6)

    display.update()


# Main programme for testing purposes
if __name__ == "__main__":
    draw_qr_file()
