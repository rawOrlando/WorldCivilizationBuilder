from tests import WCBTestCase
from db.civilization import Civilization, Settlement
from db.disaster import Disaster, CurrentDisaster
from db.map import Tile
from db.technology import Technology, CivTec
from resources import ResourceBundle
from resources.assets import (
    FOREST_NAME,
    TROPICAL_FOREST_NAME,
    RIVER_NAME,
    SHORE_NAME,
    PLAINS_NAME,
    HILL_NAME,
)
from resources.generate import (
    generate_resources_from_tile,
    generate_resources_from_settlement,
)


class TestGenerateResourcesFromTiles(WCBTestCase):
    def test_generate_resources_from_tropical_forests(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(
            x=0, y=0, z=0, controler_id=civ.id, resources=[TROPICAL_FOREST_NAME]
        )
        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(1, resources.food)
        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()

    def test_generate_resources_from_rivers(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[RIVER_NAME])
        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(1, resources.water)
        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()

    def test_generate_resources_from_forests(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[FOREST_NAME])
        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()

    def test_generate_resources_from_plains(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[PLAINS_NAME])
        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()

    def test_generate_resources_from_shore(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[SHORE_NAME])
        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()

    def test_generate_resources_from_hills(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[HILL_NAME])
        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()

    def test_generate_resources_from_hunting(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[PLAINS_NAME])
        tec = CivTec.create(
            technology_id=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            civilization_id=civ.id,
            active=True,
        )

        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)

        self.assertEqual(0, resources.water)
        self.assertEqual(1, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()
        tec.delete()

    def test_generate_resources_from_hunting_with_dogs(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[PLAINS_NAME])
        tile2 = Tile.create(
            x=-1, y=1, z=0, controler_id=civ.id, resources=[FOREST_NAME]
        )
        tec = CivTec.create(
            technology_id=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            civilization_id=civ.id,
            active=True,
        )
        tec2 = CivTec.create(
            technology_id=Technology.get(name=Technology.DOMESTICATED_DOGS_NAME).id,
            civilization_id=civ.id,
            active=True,
        )

        resource_bundle = ResourceBundle()

        resources = generate_resources_from_tile(civ, tile, resource_bundle)
        resources = generate_resources_from_tile(civ, tile2, resources)

        self.assertEqual(0, resources.water)
        self.assertEqual(1.25 * 2, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()
        tile2.delete()
        tec.delete()
        tec2.delete()

    def test_generate_resources_from_river_fishing(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[RIVER_NAME])
        tec = CivTec.create(
            technology_id=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            civilization_id=civ.id,
            active=True,
        )

        resources = generate_resources_from_tile(civ, tile, ResourceBundle())

        self.assertEqual(1, resources.water)
        self.assertEqual(0.25, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()
        tec.delete()

    def test_generate_resources_from_river_during_draught(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[RIVER_NAME])
        tec = CivTec.create(
            technology_id=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            civilization_id=civ.id,
            active=True,
        )
        c_disaster = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.DRAUGHT().id,
            start_time=0,
            end_time=12,
        )

        resources = generate_resources_from_tile(civ, tile, ResourceBundle())

        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.leather)
        self.assertEqual(0, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()
        tec.delete()
        c_disaster.delete()


class TestGenerateResourcesFromSettlement(WCBTestCase):
    def test_generate_resources_from_basic_settlements(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[FOREST_NAME])
        tile2 = Tile.create(
            x=-1, y=1, z=0, controler_id=civ.id, resources=[FOREST_NAME]
        )
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=tile.id
        )
        capital = Settlement.create(
            name="capital", civilization_id=civ.id, location_id=tile.id, is_capital=True
        )

        resources = generate_resources_from_settlement(settlement, ResourceBundle())

        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.leather)
        self.assertEqual(2, resources.wildcard)

        # Check capital generates more
        resources = generate_resources_from_settlement(capital, ResourceBundle())
        self.assertEqual(3, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()
        tile2.delete()
        settlement.delete()
        capital.delete()

    def test_generate_resources_from_settlements_durring_epidemic(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id, resources=[FOREST_NAME])
        tile2 = Tile.create(
            x=-1, y=1, z=0, controler_id=civ.id, resources=[FOREST_NAME]
        )
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=tile.id
        )
        capital = Settlement.create(
            name="capital", civilization_id=civ.id, location_id=tile.id, is_capital=True
        )
        c_disaster = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.DISEASE_OUTBREAK().id,
            start_time=0,
            end_time=12,
        )

        resources = generate_resources_from_settlement(settlement, ResourceBundle())

        self.assertEqual(0, resources.food)
        self.assertEqual(0, resources.water)
        self.assertEqual(0, resources.leather)
        self.assertEqual(1, resources.wildcard)

        # Check capital generates more
        resources = generate_resources_from_settlement(capital, ResourceBundle())
        self.assertEqual(1, resources.wildcard)

        # clean up
        civ.delete()
        tile.delete()
        tile2.delete()
        settlement.delete()
        capital.delete()
        c_disaster.delete()
