from .service import StandAloneService
from .beautify import beautify

if __name__ == "__main__":
    # start_monitoring()

    service = StandAloneService()
    requested = service.request_setup_code_if_needed()
    if requested:
        service.association_phase()
    service.operational_phase()

    while True:
        value = input("Press Enter to continue")
        data = service.retrieve_data()
        beautify(data)
        # service.send_get_status(1067)
