from .service import StandAloneService
from .vimar.utils.logger import log_info
from .vimar.utils.thread_monitor import start_monitoring
from .vimar.utils.beautify import beautify

if __name__ == "__main__":
    start_monitoring()

    service = StandAloneService()
    service.request_status_code_if_needed()
    service.start()
    
    while True:
        value = input("Press Enter to continue")
        data = service.retrieve_data()
        log_info(__name__, beautify(data))
        
