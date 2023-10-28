from global_constants import BADGE_ASSETS_DIRECTORY
import os
import display

# ------------------------------
#      Badge settings
# ------------------------------

IMAGE_WIDTH = 102
WIDTH, HEIGHT = display.WIDTH, display.HEIGHT

BORDER_SIZE = 1

COMPANY_HEIGHT = 25
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 3
DETAILS_TEXT_SIZE = 2


# Clear display and draw text sections
def draw_badge_text(skew: str = "normal") -> None:
    # Clear display
    display.clear()

    # Load text
    badge_file = [
        f for f in os.listdir(f"/{BADGE_ASSETS_DIRECTORY}/{skew}") if f.endswith(".txt")
    ][0]

    try:
        with open(f"/{BADGE_ASSETS_DIRECTORY}/{skew}/{badge_file}", "r") as f:
            company = f.readline()
            name = f.readline()
            detail1 = f.readline()
            detail2 = f.readline()
            detail3 = f.readline()
            detail4 = f.readline()
    except NameError:
        print("Badge file not found!")
        return

    display.draw_centered_text(
        company,
        "bitmap6",
        15,
        0,
        (COMPANY_HEIGHT // 2) - 10,
        WIDTH - IMAGE_WIDTH + 2 * BORDER_SIZE,
        COMPANY_TEXT_SIZE,
    )

    # Draw a white background behind the name
    display.draw_rectangle(15, 1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw name
    display.draw_text_fit_width(
        name,
        "bitmap14_outline",
        0,
        BORDER_SIZE + 1,
        COMPANY_HEIGHT,
        WIDTH - IMAGE_WIDTH - BORDER_SIZE,
        6,
    )

    # Draw white backgrounds behind the details
    display.draw_rectangle(
        15, 1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1
    )
    display.draw_rectangle(
        15, 1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1
    )

    # Details line 1
    # Computations of widths to get offset
    details_length_1 = display.measure_text(detail1, "bitmap6", DETAILS_TEXT_SIZE)
    details_length_2 = display.measure_text(detail2, "bitmap6", DETAILS_TEXT_SIZE)
    offset = WIDTH - IMAGE_WIDTH - 3 - details_length_1 - details_length_2

    # Draw text
    display.draw_text(
        detail1,
        "bitmap6",
        0,
        BORDER_SIZE + 2,
        HEIGHT - ((DETAILS_HEIGHT * 3) // 2) - 5,
        details_length_1,
        DETAILS_TEXT_SIZE,
    )

    display.draw_text(
        detail2,
        "bitmap6",
        0,
        BORDER_SIZE + 2 + details_length_1 + offset,
        HEIGHT - ((DETAILS_HEIGHT * 3) // 2) - 5,
        details_length_2,
        DETAILS_TEXT_SIZE,
    )

    # Details line 2
    # Computations of widths to get offset
    details_length_1 = display.measure_text(detail3, "bitmap6", DETAILS_TEXT_SIZE)
    details_length_2 = display.measure_text(detail4, "bitmap6", DETAILS_TEXT_SIZE)
    offset = WIDTH - IMAGE_WIDTH - 3 - details_length_1 - details_length_2

    # Draw text
    display.draw_text(
        detail3,
        "bitmap6",
        0,
        BORDER_SIZE + 2,
        HEIGHT - (DETAILS_HEIGHT // 2) - 6,
        details_length_1,
        DETAILS_TEXT_SIZE,
    )

    display.draw_text(
        detail4,
        "bitmap6",
        0,
        BORDER_SIZE + 2 + details_length_1 + offset,
        HEIGHT - (DETAILS_HEIGHT // 2) - 6,
        details_length_2,
        DETAILS_TEXT_SIZE,
    )


def draw_image(index: int = 0, skew: str = "normal") -> None:
    # Find images
    try:
        badge_images = [
            f
            for f in os.listdir(f"/{BADGE_ASSETS_DIRECTORY}/{skew}")
            if f.endswith(".jpg")
        ]
    except OSError:
        print(f"No badge images found for skew {skew}.")
        return

    if len(badge_images) == 0:
        print(f"No badge images found for skew {skew}.")
        return

    image_path = (
        f"/{BADGE_ASSETS_DIRECTORY}/{skew}/{badge_images[index % len(badge_images)]}"
    )

    # Draw image
    display.draw_image(image_path, WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    display.draw_empty_rectangle(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, HEIGHT)


# Draw the badge, including user text
def draw_badge(index: int = 0, skew: str = "normal", full_update=True) -> None:
    draw_image(index, skew)

    if full_update:
        draw_badge_text(skew)
        draw_image(index, skew)
        display.update()
    else:
        display.partial_update(WIDTH - IMAGE_WIDTH, 0, IMAGE_WIDTH, HEIGHT)


# Main programme for testing purposes
if __name__ == "__main__":
    draw_badge()
