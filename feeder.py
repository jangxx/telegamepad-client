import socket, struct

def feed_inputs(server_addr, server_port, gamepad_id, device, keymap_file, server_protocol):
    addr = server_addr + ":" + str(server_port)

    if server_protocol == "udp":
        sock = socket.socket(type=socket.SOCK_DGRAM)
    elif server_protocol == "tcp":
        sock = socket.socket(type=socket.SOCK_STREAM)
        sock.connect(addr)

    for events in device:
        for ev in events:
            print(ev.code, ev.state, ev.ev_type)