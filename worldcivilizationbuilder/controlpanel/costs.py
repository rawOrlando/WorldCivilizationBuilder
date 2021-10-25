from controlpanel.models import Civilization, Technology, Tile
from disasters.disaster import during_forest_fire
import math


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
                "cost": int(cost),
            }
            maintance_projects.append(maintance)
    for civtec in civilization.civtec.all():
        if not civtec.maintaned and civtec.needed_maintance > 0:
            maintance = {
                "name": civtec.technology.name,
                "id": "tech_" + str(civtec.id),
                "cost": int(civtec.needed_maintance),
            }
            maintance_projects.append(maintance)

    return maintance_projects


def calculate_maintance_cost_for_tile(tile, settlement_locations=None, simple=False):
    """

    Note:
    if there are no settlements it reurn infite whic is bad.
    """
    smallest_distance = calculate_distance_to_closest_settlement(
        tile, settlement_locations
    )
    cost = 1 + smallest_distance * 2
    if not simple:
        if during_forest_fire(tile.controler) and (tile.forest or tile.tropical_forest):
            cost += 1
            # Todo factor in distance to water...?
    return cost


def calculate_maintance_cost_for_tile_2(tile, settlement_locations=None, simple=False):
    """
    Todo: this should replace calculate_maintance_cost_for_tile
    Note:
    if there are no settlements it reurn infite whic is bad.
    """
    smallest_distance = calculate_distance_to_closest_settlement_2(
        tile, settlement_locations
    )
    from controlpanel.resource_names import FOREST_NAME, TROPICAL_FOREST_NAME

    cost = 1 + smallest_distance * 2
    if not simple:
        if during_forest_fire(tile.controler) and (
            tile.has(FOREST_NAME) or tile.has(TROPICAL_FOREST_NAME)
        ):
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


def calculate_distance_to_closest_settlement_2(tile, settlement_locations=None):
    if settlement_locations is None:
        settlement_locations = tile.controler.get_all_settlement_locations()
    smallest_distance = math.inf
    for settlement_location in settlement_locations:
        distance = tile.distance_between(Tile.get(_id=settlement_location.id))
        if smallest_distance > distance:
            smallest_distance = distance
    return smallest_distance
