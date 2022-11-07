This is a minimal distribution of an implementation of a three mode programme for the Pimoroni Badge 2040. Modes are as follows.

* Button A accesses the badge mode. 
* Button B accesses the QR code mode.
* Button C accesses a gallery mode.

All three modes support image switching by using the up and down buttons. They are heavily based on :link: [examples provided by Pimoroni](https://github.com/pimoroni/pimoroni-pico).

The code allows for multiple skews that affect all three modes. Skews are defined in the `SKEW_LIST` variable within the `global_constants.py` file and are cycled through by a simultaneous press of the up and down buttons.

Additionally, the variable `ALTERNATE_GALLERY_SKEWS` within the same file allows for the set up of additional galleries that are not associated for any skews. These are accessed by a simultaneous press of the A and C buttons.

State saving on flash has been included, thus the device will remember the current status when turned on and resume from there.

All three modes have their own asset folders, encoded in variables within the `global_constants.py` file. Within those folders, there must be one subfolder with the name of each skew, containing the relevant files depending on the mode. A minimal example with only one skew called `normal` has been included with this repo, hence everything should work as is on the device. 

The text for the QR codes and badges should follow the format of the provided examples. Images for the badge mode should have a resolution of `104x128`. Images for the gallery should have a resolution of `296x128`. They can be converted to the proper binary format using the [scripts in this folder](https://github.com/pimoroni/pimoroni-pico/tree/main/examples/badger2040/image_converter).
