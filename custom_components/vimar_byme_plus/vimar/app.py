import time
from .service.stand_alone_service import StandAloneService
from .utils.logger import log_debug
from .utils.thread_monitor import start_monitoring

if __name__ == "__main__":
    start_monitoring()

    service = StandAloneService()
    service.request_status_code_if_needed()
    service.start()
    
    while True:
        log_debug(__name__, "Still executing...")
        time.sleep(60)
