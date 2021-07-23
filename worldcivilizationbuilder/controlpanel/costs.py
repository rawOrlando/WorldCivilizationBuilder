from controlpanel.models import Civilization, Tile
from disasters.disaster import (is_in_a_draught,
                                during_forest_fire,
                                is_in_fighting,
                                durring_epidemic)
import math

def generate_resources(civilization):
    assets = {
        "Forests": 0,
        "Tropical Forests": 0,
        "Rivers": 0,
        "Shores": 0,
        "Plains": 0,
    }
    resources = 0
    for tile in civilization.tiles.all():
        for asset in tile.assets:
            assets[asset+"s"] += 1
        resources += generate_resources_from_tile(civilization, tile)

    # Generate through settlements
    for settlement in civilization.settlements.all():
        resources += generate_resources_from_settlement(settlement)

    if is_in_fighting(civilization):
        resources = resources/2

    return resources

def generate_resources_from_tile(civilization, tile):
    assets = tile.assets
    # Can't gain resources from a forest during a forest fire.
    if (during_forest_fire(civilization) and 
        ("Tropical Forest" in assets or
         "Forest" in assets)):
        return 0
    resources = 0
    # Generate food reasouces from Tropical Forests
    if "Tropical Forest" in assets:
        resources += 1
    # Generate food/water resources from Rivers
    if ("River" in assets and
        not is_in_a_draught(civilization)):
        resources += 1
    # Generat food resources from hunting
    if (civilization.can_hunt() and 
        ("Forest" in assets or "Plain" in assets) and
        not tile.settlements.count() > 0):
        resources += 1
    return resources

def generate_resources_from_settlement(settlement): 
    if durring_epidemic(settlement.civilization):
        return 0
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
        if not tile.maintaned:
            cost = calculate_maintance_cost_for_tile(tile, settlement_locations)
            maintance = {
                "name": str(tile),
                "id": "tile_" + str(tile.id),
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
    cost = 1 + smallest_distance * 2
    if (during_forest_fire(tile.controler) and
        (tile.forest or tile.tropical_forest)):
        cost += 1
        # Todo factor in distance to water...?
    return cost 

