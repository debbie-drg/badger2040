import os
import badger2040

from global_constants import SKEW_LIST, ALTERNATE_GALLERY_SKEWS, GALLERY_DIRECTORY

display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Load gallery images
IMAGES = dict()
TOTAL_GALLERY_IMAGES = dict()
for skew in SKEW_LIST + ALTERNATE_GALLERY_SKEWS:
    try:
        IMAGES[skew] = [
            f for f in os.listdir(f"/{GALLERY_DIRECTORY}/{skew}") if f.endswith(".bin")
        ]
        TOTAL_GALLERY_IMAGES[skew] = len(IMAGES[skew])
    except OSError:
        print(f"No images directory for skew {skew}")
        pass

# Blank full size image to write to
full_image = bytearray(int(296 * 128 / 8))

# ------------------------------
#        Gallery functions
# ------------------------------


def show_image(index: int, skew: str ="normal") -> None:

    if TOTAL_GALLERY_IMAGES[skew] == 0:
        print(f"No images in skew {skew}. Image will not be printed")
        return

    index %= TOTAL_GALLERY_IMAGES[skew]
    open(f"{GALLERY_DIRECTORY}/{skew}/{IMAGES[skew][index]}", "r").readinto(full_image)

    display.image(full_image)
    display.update()
