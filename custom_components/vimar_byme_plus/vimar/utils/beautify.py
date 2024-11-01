from prettytable import PrettyTable
from ..model.gateway.vimar_data import VimarData
from ..model.component.vimar_component import VimarComponent
from .logger import log_info


def beautify(data: VimarData):
    log_info(__name__, "\nLights:")
    print_table(data._lights)
    log_info(__name__, "\nDoors:")
    print_table(data._access)
    log_info(__name__, "\nCovers:")
    print_table(data._shutters)
    log_info(__name__, "\nClimate:")
    print_table(data._climates)
    log_info(__name__, "\nAudios:")
    print_table(data._audios)


def print_table(components: list[VimarComponent]):
    if not components:
        return
    header = components[0].get_table_header()
    table = PrettyTable(header)

    sorted_components = sorted(components, key=lambda obj: (obj.area, obj.name))
    for component in sorted_components:
        table.add_row(component.to_table())
    print(table)
