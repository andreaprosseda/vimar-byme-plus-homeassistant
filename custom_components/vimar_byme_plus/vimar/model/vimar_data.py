"""VIMAR supporting class for  ."""

from .byme_configuration.application import Application
from .byme_configuration.byme_configuration import ByMeConfiguration
from .byme_configuration.environment import Environment
from .vimar_application import VimarApplication, VimarType


class VimarData:
    _config: ByMeConfiguration

    def __init__(self, dict) -> None:
        """Initialize Vimar Data."""
        self.config = ByMeConfiguration(**dict)

    def __str__(self) -> str:
        """Return string representation of this class."""
        return f"Vimar Data {self.config.applications}"

    def get_entities(self, type: VimarType) -> list[VimarApplication]:
        """Return entities of provided type from configuration."""
        apps = self.config.applications
        result = list(filter(lambda app: self._is(app, type), apps))
        return self._get_vimar_applications(result)

    def _get_vimar_applications(
        self, apps: list[Application]
    ) -> list[VimarApplication]:
        vimar_apps = []
        for app in apps:
            vimar_type: VimarType = VimarType.from_id(app.category_id)
            env = self._get_environment(app)
            vimar_apps.append(VimarApplication(vimar_type, app, env))
        return vimar_apps

    def _get_vimar_application(self, app: Application) -> VimarApplication:
        env = self._get_environment(app)
        return VimarApplication(app, env)

    def _get_environment(self, app: Application) -> Environment:
        """Return environment for an application from configuration."""
        envs = self.config.environments
        return list(filter(lambda env: env.id == app.environment_id, envs))[0]

    def _is(self, app: Application, vimar_type: VimarType) -> bool:
        return app.category_id == vimar_type.value.get("id")
