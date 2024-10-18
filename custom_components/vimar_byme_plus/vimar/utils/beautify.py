from ..model.gateway.vimar_data import VimarData
from ..model.component.vimar_light import VimarLight

def beautify(data: VimarData) -> str:
    return beautify_lights(data.get_lights())
    
def beautify_lights(lights: list[VimarLight]) -> str:
    values = sorted(lights, key= lambda obj: (obj.area, obj.name))
    return "\n".join([str(value) for value in values])