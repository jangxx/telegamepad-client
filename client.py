import argparse, sys
import inputs
from interactive import interactive_config
from create_keymap import create_keymap
from feeder import feed_inputs

parser = argparse.ArgumentParser(description="Feed gamepad inputs to a TeleGamepad server running in the network")
subparsers = parser.add_subparsers(help="commands", dest="subcommand")

parser_default = subparsers.add_parser("run", help="Send gamepad inputs to the server")
parser_default.add_argument("-A", "--address", required=True, dest="address", help="Address of the server to connect to")
parser_default.add_argument("-P", "--port", dest="port", help="Port of the server to connect to (Default: 20719)", type=int, default=20719)
parser_default.add_argument("-I", "--id", required=True, dest="gamepad_id", help="Target gamepad id (needs to be setup on the server)", type=int)
parser_default.add_argument("-K", "--keymap", dest="keymap", help="Path to the keymap file. Can be created by using the create_keymap subcommand (Default: keymap.json)", default="keymap.json")
parser_default.add_argument("-D", "--device", dest="device_index", help="Index of the device in the list returned by list_devices (Default: 0).", type=int, default=0)
parser_default.add_argument("--server-protocol", dest="server_protocol", choices=["udp", "tcp"], default="udp", help="Protocol used by the server (Default: udp)")

parser_create_keymap = subparsers.add_parser("create_keymap", help="Create a keymap file by pressing some buttons on your gamepad.")
parser_create_keymap.add_argument("-K", "--keymap", dest="keymap", required=True, help="Path to the keymap file. Can be created by using the create_keymap subcommand (Default: keymap.json)", default="keymap.json")
parser_create_keymap.add_argument("-D", "--device", dest="device_index", help="Index of the device in the list returned by list_devices (Default: 0).", type=int, default=0)

parser_list_devices = subparsers.add_parser("list_devices", help="Get a list of detected devices and their indices.")

args = parser.parse_args()

print(args)
if args.subcommand == "list_devices":
    if len(inputs.devices.gamepads) == 0:
        print("No gamepads detected.")
        sys.exit(0)

    print("Connected gamepads (index: name):")
    for i,device in enumerate(inputs.devices.gamepads):
        print("{index}: {name} ({devpath})".format(index=i, name=device, devpath=device.get_char_device_path()))

elif args.subcommand == "create_keymap":
    if len(inputs.devices.gamepads) == 0:
        print("No gamepads detected.")
        sys.exit(1)

    if not (0 <= args.device_index < len(inputs.devices.gamepads)):
        print("Gamepad with index {index} could not be found".format(index=args.device_index))
        sys.exit(1)

    device = inputs.devices.gamepads[args.device_index]

    create_keymap(device, args.keymap)

elif args.subcommand is None:
    interactive_config()

elif args.subcommand == "run":
    if len(inputs.devices.gamepads) == 0:
        print("No gamepads detected.")
        sys.exit(1)

    if not (0 <= args.device_index < len(inputs.devices.gamepads)):
        print("Gamepad with index {index} could not be found".format(index=args.device_index))
        sys.exit(1)

    device = inputs.devices.gamepads[args.device_index]

    feed_inputs(args.address, args.port, args.gamepad_id, device, args.keymap, args.server_protocol)