import display
import os

from global_constants import GALLERY_DIRECTORY

# ------------------------------
#        Gallery functions
# ------------------------------


def show_image(index: int = 0, skew: str = "normal") -> None:
    try:
        IMAGES = [
            f for f in os.listdir(f"/{GALLERY_DIRECTORY}/{skew}") if f.endswith(".jpg")
        ]
    except OSError:
        print(f"No images directory for skew {skew}")
        return

    if len(IMAGES) == 0:
        print(f"No images in skew {skew}. Image will not be printed")
        return

    index %= len(IMAGES)
    image_path = f"{GALLERY_DIRECTORY}/{skew}/{IMAGES[index]}"

    display.clear()
    display.draw_image(image_path, 0, 0)
    display.update()


if __name__ == "__main__":
    show_image()
