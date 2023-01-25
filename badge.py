from global_constants import HEIGHT, WIDTH, SKEW_LIST, BADGE_ASSETS_DIRECTORY
import os
import badger2040

# ------------------------------
#      Badge settings
# ------------------------------

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 25
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 0.6
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL1_SPACING = dict()
DETAIL2_SPACING = dict()

# ------------------------------
#      Badge functions
# ------------------------------

DICT_BADGE_IMAGES = dict()
BADGE_IMAGES = dict()

# Load badge images for all skews
for skew in SKEW_LIST:
    try:
        BADGE_IMAGES[skew] = [
            f
            for f in os.listdir(f"/{BADGE_ASSETS_DIRECTORY}/{skew}")
            if f.endswith(".bin")
        ]
        DICT_BADGE_IMAGES[skew] = len(BADGE_IMAGES[skew])
    except OSError:
        print(f"No badge images found for skew {skew}.")
        pass

# Blank badge image to write to before drawing:
badge_image = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))


# Load text files
badge_text_files = dict()
for skew in SKEW_LIST:
    try:
        badge_text_files[skew] = [
            f
            for f in os.listdir(f"/{BADGE_ASSETS_DIRECTORY}/{skew}")
            if f.endswith(".txt")
        ]
        if len(badge_text_files[skew]) > 1:
            print(
                f"Only one file can be used per skew. Found more than one file in skew {skew}"
            )
        badge_text_files[skew] = badge_text_files[skew][0]
    except OSError:
        print(f"No text found for skew {skew}.")
        pass


# Reduce the size of a string until it fits within a given width
def truncatestring(text: str, text_size: int, width: int):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text
    return text


# Read in the badge details for all skews
company, name, detail1_title, detail1_text, detail2_title, detail2_text = (
    dict(),
    dict(),
    dict(),
    dict(),
    dict(),
    dict(),
)
for skew in SKEW_LIST:
    with open(f"/{BADGE_ASSETS_DIRECTORY}/{skew}/{badge_text_files[skew]}", "r") as f:
        company[skew] = f.readline()
        name[skew] = f.readline()
        detail1_title[skew] = f.readline()
        detail1_text[skew] = f.readline()
        detail2_title[skew] = f.readline()
        detail2_text[skew] = f.readline()

display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Truncate all of the text (except for the name as that is scaled)
for skew in SKEW_LIST:
    company[skew] = truncatestring(company[skew], COMPANY_TEXT_SIZE, TEXT_WIDTH)

    detail1_title[skew] = truncatestring(
        detail1_title[skew], DETAILS_TEXT_SIZE, TEXT_WIDTH
    )
    detail1_text[skew] = truncatestring(
        detail1_text[skew],
        DETAILS_TEXT_SIZE,
        TEXT_WIDTH - display.measure_text(detail1_title[skew], DETAILS_TEXT_SIZE),
    )

    detail2_title[skew] = truncatestring(
        detail2_title[skew], DETAILS_TEXT_SIZE, TEXT_WIDTH
    )
    detail2_text[skew] = truncatestring(
        detail2_text[skew],
        DETAILS_TEXT_SIZE,
        TEXT_WIDTH - display.measure_text(detail2_title[skew], DETAILS_TEXT_SIZE),
    )

# Compute spacing between detail text
display.font("sans")
distance_detail1 = (
    TEXT_WIDTH
    - display.measure_text(detail1_title[skew])
    - display.measure_text(detail1_text[skew])
)
distance_detail2 = (
    TEXT_WIDTH
    - display.measure_text(detail2_title[skew])
    - display.measure_text(detail2_text[skew])
)


# Draw the badge, including user text
def draw_badge(index: int = 0, skew: str = "normal", full_update: bool = True) -> None:
    display.pen(0)
    display.clear()

    if DICT_BADGE_IMAGES[skew] == 0:
        print(f"No image files for skew {skew}. Not updating.")
        return None

    index = index % DICT_BADGE_IMAGES[skew]
    open(f"{BADGE_ASSETS_DIRECTORY}/{skew}/{BADGE_IMAGES[skew][index]}", "rb").readinto(
        badge_image
    )

    # Draw badge image
    display.image(badge_image, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    if full_update:
        # Draw the header
        display.pen(15)  # Change this to 0 if a white background is used
        display.font("bitmap6")
        display.thickness(1)
        display.text(
            company[skew],
            LEFT_PADDING + 10,
            (COMPANY_HEIGHT // 2) - 10,
            COMPANY_TEXT_SIZE + 2.4,
        )

        # Draw a white background behind the name
        display.pen(15)
        display.thickness(1)
        display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

        # Draw the name, scaling it based on the available width
        display.pen(0)
        display.font("bitmap14_outline")
        display.thickness(2)
        name_size = 10  # A sensible starting scale
        while True:
            name_length = display.measure_text(name[skew], name_size)
            if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
                name_size -= 0.01
            else:
                display.text(
                    name[skew],
                    (TEXT_WIDTH - name_length) // 2 + 5,
                    (NAME_HEIGHT // 2) + COMPANY_HEIGHT - 33,
                    name_size,
                )
                break

        # Draw a white backgrounds behind the details
        display.pen(15)
        display.thickness(1)
        display.rectangle(
            1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1
        )
        display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

        # Draw the first detail's title and text
        display.pen(0)
        display.font("sans")
        display.thickness(2)
        name_length = display.measure_text(detail1_title[skew], DETAILS_TEXT_SIZE)
        display.text(
            detail1_title[skew],
            LEFT_PADDING,
            HEIGHT - ((DETAILS_HEIGHT * 3) // 2),
            DETAILS_TEXT_SIZE,
        )
        display.thickness(2)
        display.text(
            detail1_text[skew],
            LEFT_PADDING + name_length + 40,
            HEIGHT - ((DETAILS_HEIGHT * 3) // 2),
            DETAILS_TEXT_SIZE,
        )

        # Draw the second detail's title and text
        display.thickness(2)
        name_length = display.measure_text(detail2_title[skew], DETAILS_TEXT_SIZE)
        display.text(
            detail2_title[skew],
            LEFT_PADDING,
            HEIGHT - (DETAILS_HEIGHT // 2),
            DETAILS_TEXT_SIZE,
        )
        display.thickness(2)
        display.text(
            detail2_text[skew],
            LEFT_PADDING + name_length + 40,
            HEIGHT - (DETAILS_HEIGHT // 2),
            DETAILS_TEXT_SIZE,
        )

        display.update()

    else:
        display.partial_update(WIDTH - IMAGE_WIDTH, 0, IMAGE_WIDTH, HEIGHT)


# Draw the badge, including user text
def update_badge(index: int = 0, skew: str = "normal") -> None:

    if DICT_BADGE_IMAGES[skew] == 0:
        print(f"No image files for skew {skew}. Not updating.")
        return None

    index = index % DICT_BADGE_IMAGES[skew]
    open(f"{BADGE_ASSETS_DIRECTORY}/{skew}/{BADGE_IMAGES[skew][index]}", "rb").readinto(
        badge_image
    )

    # Draw badge image
    display.image(badge_image, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    display.partial_update(WIDTH - IMAGE_WIDTH, 0, IMAGE_WIDTH, HEIGHT)
    # display.update()


# Main programme for testing purposes
if __name__ == "__main__":
    draw_badge()
