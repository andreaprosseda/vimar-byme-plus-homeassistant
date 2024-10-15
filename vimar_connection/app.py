import time
from .service.initialization_service import InitializationService
from .utils.logger import log_debug
from .utils.thread import Thread
from .utils.thread_monitor import start_monitoring

def initialize():
    initialization_service = InitializationService()
    initialization_service.start()

if __name__ == "__main__":
    start_monitoring()
    
    vimar_thread = Thread(target=initialize, name="VimarThread")
    vimar_thread.start()
    
    while True:
        log_debug(__name__, "Still executing...")
        time.sleep(60)
        
        