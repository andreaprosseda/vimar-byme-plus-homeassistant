import threading

from .logger import log_debug


class Timer(threading.Timer):
    def __init__(self, interval, function, *args, name=None, **kwargs):
        super().__init__(interval, function, *args, **kwargs)
        self.name = name or "UnnamedTimer"
        log_debug(__name__, f"New Timer created: {self.name}")


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log_debug(__name__, f"New thread created: {self.name}")

    @staticmethod
    def get_active_threads():
        return threading.enumerate()
