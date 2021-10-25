import unittest
from db.projects import (
    Project,
    ResearchProject,
    ExplorationProject,
    SettlementProject,
    TileMaintenanceProject,
    TechnologyMaintenanceProject,
)
from db.civilization import Civilization, Settlement
from db.map import Tile
from db.technology import Technology, CivTec
from tests import WCBTestCase


class TestResearchProject(WCBTestCase):
    def test_get_created_research_project(self):
        project = ResearchProject.create(
            name="Name",
            current_year=0,
            civilization_id=None,  # todo actual have a civ here
            technology_type="Technology",
        )
        got_project = Project.get(_id=project.id)

        # check that they are the same.
        self.assertEqual(project.id, got_project.id)
        self.assertEqual(project.name, got_project.name)
        self.assertEqual(project.last_spent, got_project.last_spent)
        self.assertEqual(project.civilization_id, got_project.civilization_id)
        self.assertEqual(project.technology_type, got_project.technology_type)
        self.assertEqual(project.spent, got_project.spent)

        # clean up
        project.delete()


class TestExplorationProject(WCBTestCase):
    def test_get_created_exploration_project(self):
        project = ExplorationProject.create(
            name="Name",
            current_year=0,
            civilization_id=None,  # todo actual have a civ here
            territory_id=None,  # todo actual have a tile here
        )
        got_project = Project.get(_id=project.id)

        # check that they are the same.
        self.assertEqual(project.id, got_project.id)
        self.assertEqual(project.name, got_project.name)
        self.assertEqual(project.last_spent, got_project.last_spent)
        self.assertEqual(project.civilization_id, got_project.civilization_id)
        self.assertEqual(project.territory_id, got_project.territory_id)
        self.assertEqual(project.spent, got_project.spent)

        # clean up
        project.delete()


class TestSettlementProject(WCBTestCase):
    def test_get_created_exploration_project(self):
        civ = Civilization.create(name="Temp civ")
        # todo add locations
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=None
        )
        project = SettlementProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,  # todo actual have a civ here
            settlement_id=settlement.id,  # todo actual have a settlement here
        )
        got_project = Project.get(_id=project.id)

        # check that they are the same.
        self.assertEqual(project.id, got_project.id)
        self.assertEqual(project.name, got_project.name)
        self.assertEqual(project.needed, got_project.needed)
        self.assertEqual(project.last_spent, got_project.last_spent)
        self.assertEqual(project.civilization_id, got_project.civilization_id)
        self.assertEqual(project.settlement_id, got_project.settlement_id)
        self.assertEqual(project.spent, got_project.spent)

        # clean up
        project.delete()
        # settlemnt is alreasdy deletee because project failed
        settlement.delete()
        civ.delete()


class TestTileMaintenanceProject(WCBTestCase):
    def test_get_created_tile_maintenance_project(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id)
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=tile.id
        )

        project = TileMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,
            tile_id=tile.id,
        )
        got_project = Project.get(_id=project.id)

        # check that they are the same.
        self.assertEqual(project.id, got_project.id)
        self.assertEqual(project.name, got_project.name)
        self.assertEqual(project.needed, got_project.needed)
        self.assertEqual(project.last_spent, got_project.last_spent)
        self.assertEqual(project.civilization_id, got_project.civilization_id)
        self.assertEqual(project.tile_id, got_project.tile_id)
        self.assertEqual(project.spent, got_project.spent)
        self.assertEqual(project.maintenance_window, got_project.maintenance_window)
        self.assertEqual(project.last_maintained, got_project.last_maintained)

        # clean up
        civ.delete()
        tile.delete()
        settlement.delete()
        project.delete()

    def test_tile_maintenance_project_needed_value_calculated(self):
        civ = Civilization.create(name="Temp civ")
        tile = Tile.create(x=0, y=0, z=0, controler_id=civ.id)
        tile2 = Tile.create(x=-1, y=1, z=0, controler_id=civ.id)
        tile3 = Tile.create(x=-2, y=-1, z=3, controler_id=civ.id)
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=tile.id
        )
        project = TileMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,
            tile_id=tile.id,
        )
        project2 = TileMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,
            tile_id=tile2.id,
        )
        project3 = TileMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,
            tile_id=tile3.id,
        )

        # check the costs calculated correctly.
        self.assertEqual(project.needed, 1)
        self.assertEqual(project2.needed, 3)
        self.assertEqual(project3.needed, 7)

        # clean up
        civ.delete()
        tile.delete()
        tile2.delete()
        settlement.delete()
        project.delete()
        project2.delete()


class TestTechnologyMaintenanceProject(WCBTestCase):
    def test_get_created_exploration_project(self):
        civ = Civilization.create(name="Temp civ")
        tech = Technology.create(
            name=Technology.TANNING_NAME,
            tech_type="Technology",
            description="...",
        )
        civ_tech = CivTec.create(technology_id=tech.id, civilization_id=civ.id)  # todo
        project = TechnologyMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=civ.id,
            civ_tech=civ_tech,
        )
        got_project = Project.get(_id=project.id)

        # check that they are the same.
        self.assertEqual(project.id, got_project.id)
        self.assertEqual(project.name, got_project.name)
        self.assertEqual(project.needed, got_project.needed)
        self.assertEqual(project.last_spent, got_project.last_spent)
        self.assertEqual(project.civilization_id, got_project.civilization_id)
        self.assertEqual(project.technology_id, got_project.technology_id)
        self.assertEqual(project.spent, got_project.spent)
        self.assertEqual(project.maintenance_window, got_project.maintenance_window)
        self.assertEqual(project.last_maintained, got_project.last_maintained)

        # clean up
        project.delete()
        tech.delete()
        civ_tech.delete()
        civ.delete()
