import io
import signal
from contextlib import redirect_stdout


class RunWithoutInterrupt:

    def __init__(self):
        self.interupted = False

    def handler(self, signum, frame):
        self.interupted = True

    def __enter__(self):
        self.old_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.handler)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        signal.signal(signal.SIGINT, self.old_handler)
        if self.interupted:
            raise KeyboardInterrupt
        return False


class Silence:
    def __enter__(self):
        self.re = redirect_stdout(io.StringIO())
        return self.re.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return self.re.__exit__(exc_type, exc_value, traceback)
