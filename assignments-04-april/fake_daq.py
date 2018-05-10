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

            x = np.arange(0, 3e-6, 2.5e-9)
            y = np.random.normal(size=x.shape)

            self.queue.put({'x': x, 'y': y})


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
