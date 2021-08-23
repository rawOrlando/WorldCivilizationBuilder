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
