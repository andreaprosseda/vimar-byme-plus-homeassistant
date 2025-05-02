from ...model.component.vimar_cover import CoverEntityFeature
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_shutter_without_position_mapper import SsShutterWithoutPositionMapper


class SsShutterSlatWithoutPositionMapper(SsShutterWithoutPositionMapper):
    SSTYPE = SsType.SHUTTER_SLAT_WITHOUT_POSITION.value

    def get_supported_features(
        self, component: UserComponent
    ) -> list[CoverEntityFeature]:
        """Flag media player features that are supported."""
        features: list = super().get_supported_features(component)
        features.extend(
            [
                CoverEntityFeature.CLOSE_TILT,
                CoverEntityFeature.OPEN_TILT,
            ]
        )
        return features
