from .model.application import Application
from .model.environment import Environment


class VimarApplication:
    application: Application
    environment: Environment

    def __init__(self, app: Application, env: Environment) -> None:
        """Initialize Vimar Data."""
        self.application = app
        self.environment = env
