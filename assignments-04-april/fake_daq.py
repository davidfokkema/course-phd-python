"""Fake data acquisition application.

When you run this module, it will just spit out fake events on the console. You
can also import this module and use the :class:`DataAcquistion` class in an
application. As an example, this class is used in the :mod:`daq_gui` script.
"""

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
        """Create instance.

        :param queue: a :class:`multiprocessing.Queue` instance which will
            receive the event data.
        :param must_shutdown: a :class:`multiprocessing.Event` instance. When
            set, the data acquisition process will shut itself downself.

        """
        super().__init__(*args, **kwargs)

        self.queue = queue
        self.must_shutdown = must_shutdown

    def run(self):
        """Event loop for the data acquisition process.

        Sleep for a short random duration and then put a fake scintillator
        event on the queue.

        """
        # ignore SIGINT (or Ctrl-C) signals. Only the main process will capture
        # these signals and signal a shutdown.
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        while not self.must_shutdown.is_set():
            time.sleep(random.uniform(0, 2))
            x, y = self.create_fake_event()
            self.queue.put({'x': x, 'y': y})

    @classmethod
    def create_fake_event(self):
        """Create a fake event.

        The fake event resembles a flash of light in a scintillator, detected
        by a photomultiplier.

        :returns: (x, y) tuple containing the event data

        """
        # time axis, from 0 to 3 us in steps of 5 ns
        x = np.arange(0, 3e-6, 5e-9)
        # some gaussian distributed noise
        noise = np.random.normal(size=x.shape, scale=2)
        # pulseheight of the event between 30 and 500 mV
        pulseheight = np.random.uniform(low=30, high=500)
        # the signal has a very steep rise and dies out exponentially
        signal = -pulseheight * np.exp(-5e6 * x)

        # add the signal to the noise, shifted 50 samples to the right
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
