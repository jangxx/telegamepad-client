import json

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
]

def create_keymap(device, path):
    pass