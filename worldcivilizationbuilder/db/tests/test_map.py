from db.map import Tile
from tests import WCBTestCase
from db.projects import TileMaintenanceProject


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

    def test_tile_get_neighbors(self):
        tile = Tile.create(x=00, y=0, z=00)
        tile2 = Tile.create(x=1, y=-1, z=0)
        other = Tile.create(x=20, y=-10, z=-10)
        self._assert_neighbors_are_correct(tile, tile.get_neighbors())
        self._assert_neighbors_are_correct(tile2, tile2.get_neighbors())
        self._assert_neighbors_are_correct(other, other.get_neighbors())

        # clean up the tiles
        tile.delete()
        tile2.delete()
        other.delete()
        other.delete()
        # to clean up all the neighbors?

    def _assert_neighbors_are_correct(self, tile, neighbors):
        for neighbor in neighbors:
            self.assertEqual(tile.distance_between(neighbor), 1)
        self.assertEqual(len(neighbors), 6)
        # todo more..?

    def test_tile_being_claimed(self):
        tile = Tile.create(x=0, y=0, z=0)
        self.assertFalse(tile.being_claimed)

        # Create a project for this.
        project = TileMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=None,  # todo actual have a civ here
            tile_id=tile.id,
        )

        self.assertTrue(tile.being_claimed)

        # clean up the tiles
        tile.delete()
        project.delete()
