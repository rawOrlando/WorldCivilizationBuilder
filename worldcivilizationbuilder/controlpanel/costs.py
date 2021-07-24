from controlpanel.models import Civilization, Tile
from disasters.disaster import (is_in_a_draught,
                                during_forest_fire,
                                is_in_fighting,
                                durring_epidemic)
import math

class ResourceBundle:
    """ 
    Assume
    food 
    water
    and wildcard exist
    """
    def __init__(self): 
        self.food = 0.0
        self.water = 0.0
        self.wildcard = 0.0

    def simmple_total(self):
        return int(self.food) + int(self.water) + int(self.wildcard)

def generate_resources(civilization):
    assets = {
        "Forests": 0,
        "Tropical Forests": 0,
        "Rivers": 0,
        "Shores": 0,
        "Plainss": 0, # todo figure (ss) out?
    }
    resources = 0
    resource_bundle = ResourceBundle()
    for tile in civilization.tiles.all():
        for asset in tile.assets:
            assets[asset+"s"] += 1
        # I dont like how is changedbehind the scene
        resource_bundle = generate_resources_from_tile(civilization, tile, resource_bundle)
    # Generate through settlements
    print(resource_bundle.food)
    for settlement in civilization.settlements.all():
        resource_bundle = generate_resources_from_settlement(settlement, resource_bundle)
    resources = resource_bundle.simmple_total()
    if is_in_fighting(civilization):
        resources = resources/2

    return resources

def generate_resources_from_tile(civilization, tile, resource_bundle):
    assets = tile.assets
    # Can't gain resources from a forest during a forest fire.
    if (during_forest_fire(civilization) and 
        ("Tropical Forest" in assets or
         "Forest" in assets)):
        return 0
    # Generate food reasouces from Tropical Forests
    if "Tropical Forest" in assets:
        resource_bundle.food += 1
    # Generate food/water resources from Rivers
    if ("River" in assets and
        not is_in_a_draught(civilization)):
        resource_bundle.water += 1
        if civilization.can_spear_fish():
            resource_bundle.food += 0.25
    # Generat food resources from hunting
    if (civilization.can_hunt() and 
        ("Forest" in assets or "Plains" in assets) and
        not tile.settlements.count() > 0):
        resource_bundle.food += 1
    return resource_bundle

def generate_resources_from_settlement(settlement, resource_bundle): 
    if durring_epidemic(settlement.civilization):
        return 0

    if settlement.being_built:
        return 0

    # overly simple first pass
    if settlement.is_capital:
        resource_bundle.wildcard += 3
    else:
        resource_bundle.wildcard += 2
    return resource_bundle

def get_maintance_projects(civilization):
    maintance_projects = []

    # get all maintance projects for maintianing land
    # get all settlements locations
    settlement_locations = civilization.get_all_settlement_locations()
    for tile in civilization.tiles.all():
        if not tile.maintaned:
            cost = calculate_maintance_cost_for_tile(tile, settlement_locations)
            maintance = {
                "name": str(tile),
                "id": "tile_" + str(tile.id),
                "cost": int(cost)
            }
            maintance_projects.append(maintance)

    return maintance_projects

def calculate_maintance_cost_for_tile(tile, settlement_locations=None, simple=False):
    smallest_distance = calculate_distance_to_closest_settlement(tile, settlement_locations)
    cost = 1 + smallest_distance * 2
    if not simple:
        if (during_forest_fire(tile.controler) and
            (tile.forest or tile.tropical_forest)):
            cost += 1
            # Todo factor in distance to water...?
    return cost 

def calculate_distance_to_closest_settlement(tile, settlement_locations=None):
    if settlement_locations is None:
        settlement_locations = tile.controler.get_all_settlement_locations()
    smallest_distance = math.inf
    for settlement_location in settlement_locations:
        distance = tile.distance_between(Tile.objects.get(id=settlement_location))
        if smallest_distance > distance:
            smallest_distance = distance
    return smallest_distance

