from prettytable import PrettyTable
from ..model.gateway.vimar_data import VimarData
from ..model.component.vimar_component import VimarComponent

def beautify(data: VimarData):
    print("\nLights:")
    print_table(data._lights)
    print("\nDoors:")
    print_table(data._access)
    print("\nCovers:")
    print_table(data._shutters)
    print("\nClimate:")
    print_table(data._climates)
    
def print_table(components: list[VimarComponent]):
    if not components:
        return
    header = components[0].get_table_header()
    table = PrettyTable(header)
    for component in components:
        table.add_row(component.to_table())
    print(table)