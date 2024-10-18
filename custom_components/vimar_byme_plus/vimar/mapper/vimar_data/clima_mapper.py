from ...model.repository.user_component import UserComponent
from ...model.component.vimar_climate import VimarClima
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType

SFTYPE = SfType.CLIMA.value

class ClimaMapper:
    
    @staticmethod    
    def from_list(components: list[UserComponent]) -> list[VimarClima]:
        data = []
        return data
        for component in components:
            if component.sftype == SFTYPE:
                data.append(ClimaMapper.from_obj(component))
        return data
    
    @staticmethod    
    def from_obj(component: UserComponent) -> VimarClima:
        return VimarClima()