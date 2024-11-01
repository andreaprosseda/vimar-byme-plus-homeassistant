from .service import StandAloneService
from .vimar.utils.thread_monitor import start_monitoring
from .vimar.utils.beautify import beautify

if __name__ == "__main__":
    start_monitoring()

    service = StandAloneService()
    requested = service.request_setup_code_if_needed()
    if requested:
        service.association_phase()
    service.operational_phase()

    while True:
        value = input("Press Enter to continue")
        data = service.retrieve_data()
        beautify(data)
