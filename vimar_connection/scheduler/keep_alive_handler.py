import threading
from typing import Callable

class KeepAliveHandler:

    TIMEOUT = 90 # max 120s
    
    _timer: threading.Timer
    _callback: Callable[[], None]
    
    def __init__(self):
        self._timer = None
        self._callback = None

    def set_handler(self, callback: Callable[[], None]):
        self._callback = callback
        self._start_timer()

    def _start_timer(self):
        self._timer = threading.Timer(self.TIMEOUT, self._execute)
        self._timer.start()

    def _execute(self):
        if self._callback:
            self._callback()
        self._start_timer()
    
    def reset(self):
        if self._timer:
            self._timer.cancel()
        self._start_timer()

    def stop(self):
        if self._timer:
            self._timer.cancel()