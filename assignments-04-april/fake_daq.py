"""Fake data acquisition application."""

import multiprocessing
import random
import time

import numpy as np


class DataAcquistion(multiprocessing.Process):

    """Fake data acquisition processself.

    This process will inject fake data into a queueself.

    """

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = queue

    def run(self):
        while True:
            time.sleep(random.uniform(0, 1))

            x = np.arange(0, 3e-6, 2.5e-9)
            y = np.random.normal(size=x.shape)

            self.queue.put({'x': x, 'y': y})


class UserInterface(object):

    def __init__(self, queue):
        self.queue = queue

    def run(self):
        while True:
            data = self.queue.get()
            print(data)


if __name__ == '__main__':
    queue = multiprocessing.Queue()
    daq = DataAcquistion(queue)
    ui = UserInterface(queue)

    daq.start()
    ui.run()
