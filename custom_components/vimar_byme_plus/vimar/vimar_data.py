from .model.byme_configuration import ByMeConfiguration
from .model.application import Application
from .model.environment import Environment
from .vimar_application import VimarApplication


class VimarData:
    _config: ByMeConfiguration

    def __init__(self, dict) -> None:
        """Initialize Vimar Data."""
        self.config = ByMeConfiguration(**dict)

    def __str__(self) -> str:
        """Return string representation of this class."""
        return f"Vimar Data {self.config.applications}"

    def get_lights(self) -> list[VimarApplication]:
        """Return lights from configuration."""
        apps = self.config.applications
        result = list(filter(lambda app: app.category_id == "1", apps))
        return self._get_vimar_applications(result)

    def get_covers(self) -> list[VimarApplication]:
        """Return covers from configuration."""
        apps = self.config.applications
        covers = list(filter(lambda app: app.category_id == "2", apps))
        doors = list(filter(lambda app: app.category_id == "9", apps))
        result = covers + doors
        return self._get_vimar_applications(result)

    def get_climates(self) -> list[VimarApplication]:
        """Return climates from configuration."""
        apps = self.config.applications
        result = list(filter(lambda app: app.category_id == "4", apps))
        return self._get_vimar_applications(result)

    def _get_vimar_applications(
        self, apps: list[Application]
    ) -> list[VimarApplication]:
        vimar_apps = []
        for app in apps:
            env = self._get_environment(app)
            vimar_apps.append(VimarApplication(app, env))
        return vimar_apps

    def _get_vimar_application(self, app: Application) -> VimarApplication:
        env = self._get_environment(app)
        return VimarApplication(app, env)

    def _get_environment(self, app: Application) -> Environment:
        """Return environment for an application from configuration."""
        envs = self.config.environments
        return list(filter(lambda env: env.id == app.environment_id, envs))[0]
