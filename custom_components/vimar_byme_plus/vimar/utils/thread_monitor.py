import time

from .logger import log_info
from .thread import Thread


def monitor_threads():
    while True:
        active_threads = Thread.get_active_threads()
        names = [thread.name for thread in active_threads]
        log_info(__name__, f"Active Threads: {len(active_threads)} - {names}")
        time.sleep(5)


def start_monitoring():
    monitor_thread = Thread(target=monitor_threads, name="MonitorThread", daemon=True)
    monitor_thread.start()


def thread_exists(name: str) -> bool:
    active_threads = Thread.get_active_threads()
    names = [thread.name for thread in active_threads]
    return name in names
