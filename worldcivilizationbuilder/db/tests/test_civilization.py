from db.civilization import Civilization, Settlement
from db.map import Tile
from db.projects import SettlementProject
from db.technology import Technology, CivTec
from tests import WCBTestCase


class TestCivilization(WCBTestCase):

    # todo test should use a seperate DB.

    def test_creation_set_values(self):
        civ = Civilization.create(name="Temp test")
        self.assertEqual(civ.name, "Temp test")

        # check default values were set
        self.assertEqual(civ.last_year_updated, 0)
        self.assertEqual(civ.technologies_ids, [])

        self.assertIsNotNone(civ.id)

        # clean up
        civ.delete()

    def test_get_created_civilization(self):
        civ = Civilization.create(name="Temp test")
        got_civ = Civilization.get(_id=civ.id)

        # check that they are the same.
        self.assertEqual(civ.id, got_civ.id)
        self.assertEqual(civ.name, got_civ.name)
        self.assertEqual(civ.last_year_updated, got_civ.last_year_updated)
        self.assertEqual(civ.technologies_ids, got_civ.technologies_ids)

        # clean up
        civ.delete()

    def test_get_civilization_that_does_not_exist(self):
        civ = Civilization.get(_id="id???")

        self.assertIsNone(civ)

    def test_has_technology(self):
        civ = Civilization.create(name="Temp test")
        tec = CivTec.create(
            technology_id=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            civilization_id=civ.id,
            active=True,
        )
        self.assertTrue(civ.has_technology(Technology.BONE_TOOLS_NAME))
        self.assertFalse(civ.has_technology(Technology.FIRE_NAME))
        # Tests that is technlogies become unmaintained, It is not seen as having.
        tec.active = False
        tec.save()
        self.assertFalse(civ.has_technology(Technology.BONE_TOOLS_NAME))
        self.assertTrue(civ.has_technology_knowledge(Technology.BONE_TOOLS_NAME))

    def test_can_explore_tile(self):
        civ = Civilization.create(name="Temp test")
        river_tile = Tile.create(x=0, y=0, z=0, resources=["River"])
        forest_tile = Tile.create(x=1, y=-1, z=0, resources=["Forest"])
        shore_tile = Tile.create(x=-1, y=1, z=0, resources=["Shore"])
        ocean_tile = Tile.create(x=0, y=1, z=-1, resources=["Ocean"])

        # check with out any tech can only explore rivers.
        self.assertTrue(civ._can_explore_tile(river_tile))
        self.assertFalse(civ._can_explore_tile(forest_tile))
        self.assertFalse(civ._can_explore_tile(shore_tile))
        self.assertFalse(civ._can_explore_tile(ocean_tile))

        # check with Boiling water
        CivTec.create(
            technology_id=Technology.get(name=Technology.BOILING_WATER_NAME).id,
            civilization_id=civ.id,
            active=True,
        )
        self.assertTrue(civ._can_explore_tile(river_tile))
        self.assertFalse(civ._can_explore_tile(forest_tile))
        self.assertTrue(civ._can_explore_tile(shore_tile))
        self.assertFalse(civ._can_explore_tile(ocean_tile))

        # clean up
        civ.delete()


class TestSettlement(WCBTestCase):
    def test_creation_set_values(self):
        civ = Civilization.create(name="Temp civ")
        # todo add locations
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=None
        )

        self.assertEqual(settlement.civilization_id, civ.id)
        self.assertEqual(settlement.location_id, None)
        self.assertEqual(settlement.name, "place")

        # check default values were set
        self.assertEqual(settlement.is_capital, False)
        self.assertEqual(settlement.population, 0)

        self.assertIsNotNone(settlement.id)

        # clean up
        civ.delete()
        settlement.delete()

    def test_get_created_settlement(self):
        civ = Civilization.create(name="Temp test")
        # todo add locations
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=None
        )
        got_settlement = Settlement.get(_id=settlement.id)

        # check that they are the same.
        self.assertEqual(settlement.id, got_settlement.id)
        self.assertEqual(settlement.civilization_id, got_settlement.civilization_id)
        self.assertEqual(settlement.location_id, got_settlement.location_id)
        self.assertEqual(settlement.name, got_settlement.name)
        self.assertEqual(settlement.is_capital, got_settlement.is_capital)
        self.assertEqual(settlement.population, got_settlement.population)

        # clean up
        civ.delete()
        settlement.delete()

    def test_tile_being_claimed(self):
        civ = Civilization.create(name="Temp test")
        tile = Tile.create(x=0, y=0, z=0)
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=tile.id
        )
        self.assertFalse(settlement.being_built)

        # Create a project for this.
        project = SettlementProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,  # todo actual have a civ here
            settlement_id=settlement.id,  # todo actual have a settlement here
        )

        self.assertTrue(settlement.being_built)

        # clean up the tiles
        civ.delete()
        tile.delete()
        # project will delete settlement because it was not finished.
        project.delete()
