import socket, struct, json

def feed_inputs(server_addr, server_port, gamepad_id, device, keymap_file, server_protocol):
    addr = server_addr + ":" + str(server_port)

    with open(keymap_file, "r") as kmf:
        keymap = json.load(kmf)

    print(keymap)

    return

    if server_protocol == "udp":
        sock = socket.socket(type=socket.SOCK_DGRAM)
    elif server_protocol == "tcp":
        sock = socket.socket(type=socket.SOCK_STREAM)
        sock.connect(addr)

    for events in device:
        for ev in events:
            if ev.code in keymap:
                if ev.ev_type == "Key":
                    key_id = keymap[ev.code]["key"]

                    # todo: send data to server
                elif ev.ev_type == "Absolute":
                    key_id = keymap[ev.code]["key"]
                    scale = keymap[ev.code]["max"]

                    # todo: send data to server