from threading import Thread


class Timer:
    def __init__(self, duration, ticks):
        self.duration = duration
        self.ticks = ticks
        self.thread = None

    def start(self):
        pass
    # start Thread here
