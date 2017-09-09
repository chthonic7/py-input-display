#!/usr/bin/env python3

import asyncio
import evdev
import curses

async def print_events(device, stdscr):
    """ Cap events => print stuff """
    while True:
        events = await device.async_read()
        for event in events:
            parse_input(evdev.categorize(event), stdscr)
        stdscr.refresh()

button_map = {
        288: ['(A)', 1, 23],
        289: ['(B)', 2, 20],
        290: ['(X)', 0, 20],
        291: ['(Y)', 1, 17],
        292: ['(L)', 0, 9],
        293: ['(R)', 0, 14],
        294: ['(s)', 1, 10],
        295: ['(S)', 1, 13]
        }
dpad_map = {
        0: {
            0: ['(<)', 1, 0],
            255: ['(>)', 1, 6]
            },
        1: {
            0: ['(^)', 0, 3],
            255: ['(v)', 2, 3]
            }
        }

def parse_input(event, stdscr):
    # Capture button inputs
    if isinstance(event, evdev.events.KeyEvent):
        #print(event.scancode, event.keystate)
        button = button_map[event.scancode]
        if event.keystate == 1:
            #button = '\033[41m' + button
            stdscr.addstr(button[1],button[2], button[0], curses.color_pair(2))
        else:
            #button = '\033[40m' + button
            stdscr.addstr(button[1],button[2], button[0], curses.color_pair(1))

    # Capture d-pad inputs
    elif isinstance(event, evdev.events.AbsEvent):
        #print(event.event.code, event.event.value)
        _event = event.event
        if (_event.value == 128):
            # This script is stateless, so we don't know which direction, just the axis that was unpressed.
            # Therefore we just "unpress" both sides on the axis
            dpad = dpad_map[_event.code][0]
            stdscr.addstr(dpad[1],dpad[2], dpad[0], curses.color_pair(1))
            dpad = dpad_map[_event.code][255]
            stdscr.addstr(dpad[1],dpad[2], dpad[0], curses.color_pair(1))
        else:
            dpad = dpad_map[_event.code][_event.value] 
            stdscr.addstr(dpad[1],dpad[2], dpad[0], curses.color_pair(2))

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Unpressed
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Pressed
    curses.curs_set(0)

    # Draw up the input display for initial state
    for _, button in button_map.items():
        stdscr.addstr(button[1],button[2], button[0], curses.color_pair(1))
    for _, ddir in dpad_map.items():
        for _, dpad in ddir.items():
            stdscr.addstr(dpad[1],dpad[2], dpad[0], curses.color_pair(1))
    stdscr.refresh()

    # Sorta hardcode the controller for my computer
    controller = evdev.InputDevice('/dev/input/by-id/usb-0583_USB_2-axis_8-button_gamepad-event-joystick')

    asyncio.async(print_events(controller, stdscr))

    loop = asyncio.get_event_loop()
    loop.run_forever()

curses.wrapper(main)
