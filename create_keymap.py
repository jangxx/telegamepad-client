import json, os, math
from gamepad import GamepadReader

KEYS = [
    ("A Button", 0, "button"),
    ("B Button", 1, "button"),
    ("X Button", 2, "button"),
    ("Y Button", 3, "button"),
    ("Start Button", 4, "button"),
    ("Back Button", 5, "button"),
    ("Left Shoulder Button", 6, "button"),
    ("Right Shoulder Button", 7, "button"),
    ("Left Thumb Button", 10, "button"),
    ("Right Thumb Button", 11, "button"),
    ("Xbox Button", 12, "button"),

    ("Left Stick", 0x0100, "x-axis"),
    ("Left Stick", 0x0101, "y-axis"),
    ("Right Stick", 0x0102, "x-axis"),
    ("Right Stick", 0x0103, "y-axis"),
    ("Dpad", 0x0104, "x-axis"),
    ("Dpad", 0x0105, "y-axis"),
    ("Left Trigger", 0x0208, "trigger-axis"),
    ("Right Trigger", 0x0209, "trigger-axis"),
]

def create_keymap(device_index, path):
    if os.path.exists(path):
        print("The keymap file {path} already exists.".format(path=path))
        return

    print("Interactive keymap creation started!")
    print("Please follow the instructions to create your keymap.")
    print()

    keymap = {}

    done = False
    cur_key = 0

    pad = GamepadReader(device_index)
    pad.start()

    while not done:
        key = KEYS[cur_key]

        input_detected = None
        max_value = None

        if key[2] == "button":
            print("Please press the {button_name}".format(button_name=key[0]))

            while input_detected is None:
                ev = pad.get()

                if ev.type == "Key" and ev.state == 1:
                    input_detected = ev.code
                    break
        elif key[2] == "x-axis" or key[2] == "y-axis":
            print("Please move the {axis_name} all the way in the {direction} direction and hold it for 1 second.".format(axis_name=key[0], direction="X" if key[2] == "x-axis" else "Y"))

            input_detected, max_value = pad.get_held_axis(1)

            max_value = 2**round(math.log2(max_value)) - 1

        elif key[2] == "trigger-axis":
            print("Please push the {axis_name} all the way in and hold it for 1 second.".format(axis_name=key[0]))

            input_detected, max_value = pad.get_held_axis(1)
            max_value = 2**round(math.log2(max_value)) - 1

        while True:
            response = input("Is {button_name} correct? [Y/n] ".format(button_name=input_detected))
            if response in [ "", "y", "Y", "yes" ]:
                keymap[input_detected] = key[1] if max_value is None else { "key": key[1], "max": max_value }

                if cur_key != len(KEYS) - 1:
                    cur_key += 1
                    break
                else:
                    done = True
                    break
            elif response in [ "n", "N", "no" ]:
                break

        pad.clear_queue()

    pad.stop()

    with open(path, "w+") as keymap_file:
        json.dump(keymap, keymap_file)

    print("Your keymap has been created successfully in {path}".format(path=path))