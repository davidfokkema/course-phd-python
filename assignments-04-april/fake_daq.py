"""Fake data acquisition application."""

import multiprocessing
import random
import signal
import time

import numpy as np


class DataAcquistion(multiprocessing.Process):

    """Fake data acquisition process.

    This process will inject fake data into a queue.

    """

    def __init__(self, queue, must_shutdown, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = queue
        self.must_shutdown = must_shutdown

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        while not self.must_shutdown.is_set():
            time.sleep(random.uniform(0, 2))
            x, y = self.create_fake_event()
            self.queue.put({'x': x, 'y': y})

    @classmethod
    def create_fake_event(self):
            x = np.arange(0, 3e-6, 5e-9)
            pulseheight = np.random.uniform(low=30, high=500)
            noise = np.random.normal(size=x.shape, scale=2)
            signal = -pulseheight * np.exp(-5e6 * x)

            event = noise
            event[50:] += signal[:-50]

            return x, event


if __name__ == '__main__':
    queue = multiprocessing.Queue()
    must_shutdown = multiprocessing.Event()

    daq = DataAcquistion(queue, must_shutdown)
    daq.start()

    try:
        while True:
            data = queue.get()
            print(data)
    except KeyboardInterrupt:
        print("Shutting down.")
        must_shutdown.set()
        daq.join()
