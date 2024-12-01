from prettytable import PrettyTable
from ..model.gateway.vimar_data import VimarData
from ..model.component.vimar_component import VimarComponent
from .logger import log_info


def beautify(data: VimarData):
    log_info(__name__, "\n\nLights:")
    print_table(data._lights)
    log_info(__name__, "\n\nDoors:")
    print_table(data._access)
    log_info(__name__, "\n\nCovers:")
    print_table(data._shutters)
    log_info(__name__, "\n\nClimate:")
    print_table(data._climates)
    log_info(__name__, "\n\nAudios:")
    print_table(data._audios)
    log_info(__name__, "\n\Energies:")
    print_table(data._energies)


def print_table(components: list[VimarComponent]):
    if not components:
        return
    header = components[0].get_table_header()
    table = PrettyTable(header)

    sorted_components = sorted(components, key=lambda obj: (obj.area, obj.name))
    for component in sorted_components:
        table.add_row(component.to_table())
    print(table)


def print_elements(elements: dict):
    if not elements:
        return

    header = ["Type", "Enable", "Value"]
    cmd_table = PrettyTable(header)
    state_table = PrettyTable(header)

    sorted_components = sorted(
        elements, key=lambda obj: (obj["sfetype"], obj["enable"])
    )

    for component in sorted_components:
        values = [component["sfetype"], component["enable"], component["value"]]
        if "SFE_Cmd" in component["sfetype"]:
            cmd_table.add_row(values)
        if "SFE_State" in component["sfetype"]:
            state_table.add_row(values)

    print(cmd_table)
    print(state_table)
