from db.map import Tile
from tests import WCBTestCase


class TestTile(WCBTestCase):
    def test_get_created_tile(self):
        tile = Tile.create(x=-1100, y=0, z=1100)
        got_tile = Tile.get(_id=tile.id)

        # check that they are the same.
        self.assertEqual(tile.id, got_tile.id)
        self.assertEqual(tile.x, got_tile.x)
        self.assertEqual(tile.y, got_tile.y)
        self.assertEqual(tile.controler_id, got_tile.controler_id)
        self.assertEqual(tile.resources, got_tile.resources)

        # clean up
        tile.delete()

    def test_tile_distance_between(self):
        tile = Tile.create(x=00, y=0, z=00)
        other = Tile.create(x=20, y=-10, z=-10)
        other2 = Tile.create(x=15, y=-12, z=-3)

        # See that distance is 0 to it self
        self.assertEqual(tile.distance_between(tile), 0)

        # Check a more normal distance
        self.assertEqual(tile.distance_between(other), 20)
        self.assertEqual(other.distance_between(other2), 7)
        self.assertEqual(tile.distance_between(other2), 15)

        # make sure distance works both ways
        self.assertEqual(tile.distance_between(other), other.distance_between(tile))

        # clean up the tiles
        tile.delete()
        other.delete()
        other2.delete()
