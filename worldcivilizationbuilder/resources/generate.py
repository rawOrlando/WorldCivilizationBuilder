# from controlpanel.costs import calculate_distance_to_closest_settlement
from disasters.disaster import (
    is_in_a_draught,
    during_forest_fire,
    is_in_fighting,
    durring_epidemic,
)
from resources import ResourceBundle
from map.assets import (
    FOREST_NAME,
    TROPICAL_FOREST_NAME,
    RIVER_NAME,
    SHORE_NAME,
    PLAINS_NAME,
    HILL_NAME,
)
from db.technology import Technology

# temp
calculate_distance_to_closest_settlement = 0


def generate_resources(civilization):
    resource_bundle = ResourceBundle()
    for tile in civilization.territories():
        # I dont like how is changedbehind the scene
        resource_bundle = generate_resources_from_tile(
            civilization, tile, resource_bundle
        )
    # Generate through settlements
    for settlement in civilization.settlements():
        resource_bundle = generate_resources_from_settlement(
            settlement, resource_bundle
        )

    if is_in_fighting(civilization):
        resource_bundle = resource_bundle // 2

    return resource_bundle


def generate_resources_from_tile(civilization, tile, resource_bundle):
    assets = tile.resources
    # Can't gain resources from a forest during a forest fire.
    if during_forest_fire(civilization) and (
        TROPICAL_FOREST_NAME in assets or FOREST_NAME in assets
    ):
        return resource_bundle
    # Generate food reasouces from Tropical Forests
    if TROPICAL_FOREST_NAME in assets:
        resource_bundle.food += 1
    # Generate food/water resources from Rivers
    if RIVER_NAME in assets and not is_in_a_draught(civilization):
        resource_bundle.water += 1
        if civilization.can_spear_fish():
            resource_bundle.food += 0.25
    # Generat food resources from hunting
    if (
        civilization.can_hunt()
        and (FOREST_NAME in assets or PLAINS_NAME in assets)
        and not tile.settlements
    ):
        resource_bundle.food += 1
        if civilization.has_technology(Technology.DOMESTICATED_DOGS_NAME):
            resource_bundle.food += 0.25
        if civilization.has_technology(
            Technology.TANNING_NAME
        ) and 1 == calculate_distance_to_closest_settlement(tile):
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

    if durring_epidemic(settlement.civilization()):
        generate_wildcard = generate_wildcard // 2

    resource_bundle.wildcard += generate_wildcard
    return resource_bundle
