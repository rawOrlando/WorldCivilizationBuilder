from disasters.disaster import during_forest_fire
from map.distance import calculate_distance_to_closest_settlement
from resources.assets import FOREST_NAME, TROPICAL_FOREST_NAME


def calculate_maintance_cost_for_tile(tile, settlement_locations=None, simple=False):
    """
    Todo: this should replace calculate_maintance_cost_for_tile
    Note:
    if there are no settlements it reurn infite whic is bad.
    """
    smallest_distance = calculate_distance_to_closest_settlement(
        tile, settlement_locations
    )

    cost = 1 + smallest_distance * 2
    if not simple:
        if during_forest_fire(tile.controler()) and (
            tile.has(FOREST_NAME) or tile.has(TROPICAL_FOREST_NAME)
        ):
            cost += 1
            # Todo factor in distance to water...?
    return cost
