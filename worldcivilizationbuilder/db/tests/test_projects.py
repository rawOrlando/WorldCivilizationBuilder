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
from db.technology import Technology, CivTec
from mock import patch
from db.tests import test_db_path


@patch("db.helper.DB_PATH", new_callable=test_db_path)
class TestResearchProject(unittest.TestCase):
    def test_get_created_research_project(self, db_path):
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


@patch("db.helper.DB_PATH", new_callable=test_db_path)
class TestExplorationProject(unittest.TestCase):
    def test_get_created_exploration_project(self, db_path):
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


@patch("db.helper.DB_PATH", new_callable=test_db_path)
class TestSettlementProject(unittest.TestCase):
    def test_get_created_exploration_project(self, db_path):
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


@patch("db.helper.DB_PATH", new_callable=test_db_path)
class TestTileMaintenanceProject(unittest.TestCase):
    def test_get_created_exploration_project(self, db_path):
        project = TileMaintenanceProject.create(
            name="Name",
            current_year=0,
            civilization_id=None,  # todo actual have a civ here
            tile_id=None,  # todo actual have a tile here
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
        project.delete()


@patch("db.helper.DB_PATH", new_callable=test_db_path)
class TestTechnologyMaintenanceProject(unittest.TestCase):
    def test_get_created_exploration_project(self, db_path):
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
