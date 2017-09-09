# iBuffalo Input Display

Input Display for iBuffalo USB SNES controller for Linux written in python

## Dependencies

This script uses `curses` to draw the input display and `evdev` to poll for the inputs.
Python >=3 is required since `asyncio` is used.

`curses` should be included with Python core (at least on Linux) and `evdev` can be installed through pip.

## Running

This can be run as a normal python script and killed with ctrl-c. The script will take over your terminal because it's `curses`. Nothing fancy.
