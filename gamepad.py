import inputs, queue, time, math
from multiprocessing import Process, Queue
from collections import namedtuple

InputEvent = namedtuple("InputEvent", "code state type")

def _get_inputs(device_id, q):
    device = inputs.devices.gamepads[device_id]

    for events in device:
        for ev in events:
            q.put(InputEvent(ev.code, ev.state, ev.ev_type))

def dist_to_next_pow2(x):
    l2 = math.log2(x)
    next_pow2 = 2**round(l2)

    return abs(next_pow2 - x)

class GamepadReader:
    def __init__(self, device_id):
        self._queue = Queue()
        self._proc = Process(target=_get_inputs, args=(device_id, self._queue))

    def start(self):
        self._proc.start()

    def stop(self):
        self._proc.terminate()

    def clear_queue(self):
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass

    def get(self):
        return self._queue.get()

    def get_held_axis(self, timeout):
        held_axis = {}

        while True:
            if len(held_axis) != 0:
                t = timeout - time.perf_counter() - min(a[1] for a in held_axis.values())

                try:
                    ev = self._queue.get(True, timeout=t)
                except queue.Empty:
                    # timeout was reached i.e. an axis was held for timeout seconds
                    max_value = max(abs(a[0]) for a in held_axis.values())
                    del_axis = None

                    for axis, state in held_axis.items():
                        # print(axis, state, time.perf_counter(), time.perf_counter() - state[1])
                        if time.perf_counter() - state[1] >= timeout:
                            if abs(state[0]) == max_value and dist_to_next_pow2(max_value) <= 1:
                                return axis, max_value
                            else:
                                del_axis = axis
                                break

                    if del_axis is not None:
                        del held_axis[del_axis]
                    continue
            else:
                ev = self.get()

            if ev.type != "Absolute":
                continue

            held_axis[ev.code] = (ev.state, time.perf_counter())