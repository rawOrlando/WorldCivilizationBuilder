from db.map import Tile
import math


def calculate_distance_to_closest_settlement(tile, settlement_locations=None):
    if settlement_locations is None:
        settlement_locations = tile.controler().get_all_settlement_locations()
    smallest_distance = math.inf
    for settlement_location in settlement_locations:
        distance = tile.distance_between(Tile.get(_id=settlement_location.id))
        if smallest_distance > distance:
            smallest_distance = distance
    return smallest_distance
