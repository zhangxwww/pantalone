import signal


class RunWithoutInterrupt:

    @staticmethod
    def handler(signum, frame):
        pass

    def __enter__(self):
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        return False
