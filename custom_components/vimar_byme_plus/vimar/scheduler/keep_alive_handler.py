import threading
from typing import Callable
from ..utils.thread import Timer

class KeepAliveHandler:

    TIMEOUT = 90 # max 120s
    
    _timer: threading.Timer
    _callback: Callable[[], None]
    
    def __init__(self):
        self._timer = None
        self._callback = None

    def set_handler(self, callback: Callable[[], None]):
        self._callback = callback

    def _start_timer(self):
        if not self._timer or not self._timer.is_alive():
            self._timer = Timer(self.TIMEOUT, self._execute, name="KeepAliveHandler")
            self._timer.start()
            # self._timer = threading.Timer(self.TIMEOUT, self._execute)
            # self._timer.start()

    def _execute(self):
        if self._callback:
            self._callback()
        self._start_timer()
    
    def reset(self):
        self.stop()
        self._start_timer()

    def stop(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None