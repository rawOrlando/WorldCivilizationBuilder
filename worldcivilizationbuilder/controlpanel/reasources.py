from controlpanel.models import Civilization, Technology, Tile
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

    Should this just be a dictionary?
    """
    def __init__(self): 
        self.food = 0.0
        self.water = 0.0
        self.leather = 0.0
        self.wildcard = 0.0

    def simmple_total(self):
        return (int(self.food) + int(self.water) + 
            int(self.leather) + int(self.wildcard))

    def __floordiv__(self, other):
        self.food = self.food//other
        self.water = self.water//other
        self.leather = self.leather//other
        self.wildcard = self.wildcard//other

def generate_resources(civilization):
    assets = {
        "Forests": 0,
        "Tropical Forests": 0,
        "Rivers": 0,
        "Shores": 0,
        "Plainss": 0, # todo figure (ss) out?
        "Hills": 0
    }
    resources = 0
    resource_bundle = ResourceBundle()
    for tile in civilization.tiles.all():
        for asset in tile.assets:
            assets[asset+"s"] += 1
        # I dont like how is changedbehind the scene
        resource_bundle = generate_resources_from_tile(civilization, tile, resource_bundle)
    # Generate through settlements
    for settlement in civilization.settlements.all():
        resource_bundle = generate_resources_from_settlement(settlement, resource_bundle)

    if is_in_fighting(civilization):
        resources = resource_bundle//2

    return resource_bundle

def generate_resources_from_tile(civilization, tile, resource_bundle):
    assets = tile.assets
    # Can't gain resources from a forest during a forest fire.
    if (during_forest_fire(civilization) and 
        ("Tropical Forest" in assets or
         "Forest" in assets)):
        return resource_bundle
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
        if civilization.has_technology(Technology.DOMESTICATED_DOGS_NAME):
            resource_bundle.food += 0.25
        if (civilization.has_technology(Technology.TANNING_NAME) and
            1==calculate_distance_to_closest_settlement(tile)):
            resource_bundle.leather += 1
    return resource_bundle

def generate_resources_from_settlement(settlement, resource_bundle): 
    if settlement.being_built:
        return resource_bundle

    generate_wildcard = 0
    # overly simple first pass
    if settlement.is_capital:
        generate_wildcard += 3
    else:
        generate_wildcard += 2

    if durring_epidemic(settlement.civilization):
        generate_wildcard = generate_wildcard//2

    resource_bundle.wildcard += generate_wildcard
    return resource_bundle