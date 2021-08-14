from db.map import Tile

def distance_between(tile_a, tile_b):
	return (abs(tile_a.x - tile_b.x) + abs(tile_a.y - tile_b.y) + abs(tile_a.z - tile_b.z)) / 2


def get_neighbors(tile):
    # North +y, -z
    north = Tile.get_or_create(x=tile.x,y=tile.y+1,z=tile.z-1)
    # North East +x, -z
    north_east = Tile.get_or_create(x=tile.x+1,y=tile.y,z=tile.z-1)
    # South East +x, -y
    south_east = Tile.get_or_create(x=tile.x+1,y=tile.y-1,z=tile.z)
    # South -y, +z
    south = Tile.get_or_create(x=tile.x,y=tile.y-1,z=tile.z+1)
    # North West -x, +z
    north_west = Tile.get_or_create(x=tile.x-1,y=tile.y,z=tile.z+1)
    # South West -x, +y
    south_west = Tile.get_or_create(x=tile.x-1,y=tile.y+1,z=tile.z)

    return {north, north_east, north_west, south, south_east, south_west}