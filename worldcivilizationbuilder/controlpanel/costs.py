from controlpanel.models import Civilization, Tile
import math

def generate_resources(civilzation):
    assets = {
        "Forests": 0,
        "Tropical Forests": 0,
        "Rivers": 0,
        "Shores": 0,
        "Plains": 0,
    }
    resource = 0
    for tile in civilzation.tiles.all():
        for asset in tile.assets:
            assets[asset+"s"] += 1

    # Generate food reasouces from Tropical Forests
    resource += assets["Tropical Forests"]

    # Generate food/water resources from Rivers
    resource += assets["Rivers"]

    # Generate through settlements
    for settlement in civilzation.settlements.all():
        resource += generate_resources_from_settlement(settlement)

    return resource


def generate_resources_from_settlement(settlement): 
    # overly simple first pass
    if settlement.is_capital:
        return 3
    return 2

def get_maintance_projects(civilzation):
    maintance_projects = []

    # get all maintance projects for maintianing land
    # get all settlements locations
    settlement_locations = civilzation.settlements.all().values_list("location", flat=True).distinct()
    for tile in civilzation.tiles.all():
        cost = calculate_maintance_cost_for_tile(tile, settlement_locations)
        maintance = {
            "name": str(tile),
            "cost": int(cost)
        }
        maintance_projects.append(maintance)

    return maintance_projects

def calculate_maintance_cost_for_tile(tile, settlement_locations):
    smallest_distance = math.inf
    for settlement_location in settlement_locations:
        distance = tile.distance_between(Tile.objects.get(id=settlement_location))
        if smallest_distance > distance:
            smallest_distance = distance
    return 1 + smallest_distance * 2

