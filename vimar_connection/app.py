from .service.initialization_service import InitializationService

if __name__ == "__main__":
    initialization_service = InitializationService()
    initialization_service.start()
    # vimar_client = VimarClient(gateway_info)
    # vimar_client.connect()