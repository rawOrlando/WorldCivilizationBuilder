import unittest
from db.map import Tile
from mock import patch
from db.tests import test_db_path


@patch("db.helper.DB_PATH", new_callable=test_db_path)
class TestTile(unittest.TestCase):
    def test_get_created_tile(self, db_path):
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
