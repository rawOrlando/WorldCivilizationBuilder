from tinydb import Query
from db.base import Base_DB_Model
from db.helper import Dict2Class, get_db

from technology import unlock_another_technology

# from controlpanel.costs import calculate_maintance_cost_for_tile

import random


class Project(Base_DB_Model):
    """
    Fields:
        id                      uuid
        name                    str
        spent                   int
        last_spent              float
        needed                  int
        civilization_id         uuid

    """

    TABLE_NAME = "project"
    ## abrstact class.

    # default values
    def _set_defaults(self):
        self._set_default("spent", 0)
        super(Project, self)._set_defaults()

    @classmethod
    def create(cls, name, current_year, needed, civilization_id, spent=0):
        project = cls()
        project.name = name
        project.last_spent = current_year
        project.needed = needed
        project.civilization_id = civilization_id
        project.spent = spent
        project._set_defaults()

        return project

    def spend(self, amount):
        self.spent += amount
        current_year = self.civilization.last_year_updated
        self.last_spent = current_year

        if self._is_complete():
            self._complete(current_year)
            if not self.is_maintance():
                # should this be apart of complete
                self.delete()
            return

        self.save()

    def is_maintance(self):
        return False

    def _is_complete(self):
        return self.spent >= self.needed

    def _update(self, year):
        if self._should_decay(year):
            self._decay(year)

        if self._has_failed():
            self._fail()

    def _has_failed(self):
        return self.spent < 0

    def _fail(self):
        self.delete()

    def _should_decay(self, year):
        return int(year - self.last_spent) > 0

    def _decay(self, year):
        self.spent -= (year - self.last_spent) ** 2
        self.save()

    @classmethod
    def get(cls, _id):
        with get_db() as db:
            table = db.table(cls.TABLE_NAME)

            query = Query()
            values = table.get((query.id == _id))

            if not values:
                return None

            # to this feel hacky
            if "technology_type" in values:
                return ResearchProject.create_from_values(values)
            elif "territory_id" in values:
                return ExplorationProject.create_from_values(values)
            elif "settlement_id" in values:
                return SettlementProject.create_from_values(values)
            elif "tile_id" in values:
                return TileMaintenanceProject.create_from_values(values)
            elif "technology_id" in values:
                return TechnologyMaintenanceProject.create_from_values(values)

    def civilization(self):
        from db.civilization import Civilization

        return Civilization.get(self.civilization_id)


class ResearchProject(Project):
    """
    Fields:
        id                      uuid
        name                    str
        spent                   int
        last_spent              float
        civilization_id         uuid
        technology_type         str

    """

    @classmethod
    def create(
        cls,
        name,
        current_year,
        civilization_id,
        technology_type,
    ):
        with get_db() as db:
            table = db.table(Project.TABLE_NAME)

            project = super(ResearchProject, cls).create(
                name=name,
                current_year=current_year,
                civilization_id=civilization_id,
                needed=None,
            )
            project.technology_type = technology_type

            project._set_defaults()
            table.insert(project.__dict__)
            return project

    def _is_complete(self):
        chance = random.randrange(1, 101)
        return self.spent >= chance

    def _complete(self, year):
        civilization = self.civilization
        tech = unlock_another_technology(civilization)

        if tech.technology.needed_maintance:
            TechnologyMaintenanceProject.create(
                current_year=civilization.last_year_updated,
                civilization_id=self.civilization.id,
                civ_tech=tech,
            )


class ExplorationProject(Project):
    """
    Fields:
        id                      uuid
        name                    str
        spent                   int
        last_spent              float
        civilization_id         uuid

        territory_id            uuid

    """

    @classmethod
    def create(
        cls,
        name,
        current_year,
        civilization_id,
        territory_id,
    ):
        with get_db() as db:
            table = db.table(Project.TABLE_NAME)

            needed = 0  # todo make this be calculate on the fly
            project = super(ExplorationProject, cls).create(
                name=name,
                current_year=current_year,
                civilization_id=civilization_id,
                needed=needed,
            )
            project.territory_id = territory_id

            project._set_defaults()
            table.insert(project.__dict__)
            return project

    @property
    def territory(self):
        from db.map import Tile

        return Tile.get(self.territory_id)

    def _complete(self):
        territory = self.territory
        territory.controler_id = self.civilization_id

        TileMaintenanceProject.create(
            current_year=self.civilization.last_year_updated,
            civilization_id=self.civilization_id,
            tile_id=self.territory_id,
        )
        territory.save()


class SettlementProject(Project):
    """
    Fields:
        id                      uuid
        name                    str
        spent                   int
        last_spent              float
        civilization_id         uuid

        settlement_id           uuid

    """

    @classmethod
    def create(
        cls,
        name,
        current_year,
        civilization_id,
        settlement_id,
    ):
        with get_db() as db:
            table = db.table(Project.TABLE_NAME)

            project = super(SettlementProject, cls).create(
                name=name,
                current_year=current_year,
                civilization_id=civilization_id,
                needed=30,
            )
            project.settlement_id = settlement_id

            project._set_defaults()
            table.insert(project.__dict__)
            return project

    @property
    def settlement(self):
        from db.civilization import Settlement

        return Settlement.get(self.settlement_id)

    def delete(self):
        if not self._is_complete():
            self.settlement.delete()
        super(SettlementProject, self).delete()

    def _complete(self):
        pass
        # todo finish this thing.
        # migrate_initial_population_to_new_settlement(self.settlement)


class MaintenanceProject(Project):
    """
    add feilds last_maintained, maintenance_window
    Overload has_failed
    overload _should_decay
    """

    @classmethod
    def create(
        cls,
        name,
        current_year,
        needed,
        civilization_id,
        maintenance_window=1.0,
        spent=0,
    ):

        project = super(MaintenanceProject, cls).create(
            name=name,
            current_year=current_year,
            civilization_id=civilization_id,
            needed=needed,
        )
        project.maintenance_window = maintenance_window
        project.last_maintained = current_year

        return project

    def _should_decay(self, year):
        return year - self.last_spent > self.maintenance_window

    def is_maintance(self):
        return True

    def reset_maintance(self, year):
        self.spent = 0
        self.last_maintained = year
        self.save()

    def _complete(self, year):
        self.reset_maintance(year)


class TileMaintenanceProject(MaintenanceProject):
    """
    Fields:
        id                      uuid
        name                    str
        spent                   int
        last_spent              float
        needed                  int
        civilization_id         uuid
        maintenance_window      float
        last_maintained         float
        tile_id                 uuid

    """

    @classmethod
    def create(
        cls, current_year, civilization_id, tile_id, name=None, db=None, table=None
    ):
        with get_db() as db:
            table = db.table(TileMaintenanceProject.TABLE_NAME)

            # jank todo make better
            from db.map import Tile

            tile = Tile.get(_id=tile_id)
            if not name:
                name = "Tile Maintenace for" + str(tile)

            project = super(TileMaintenanceProject, cls).create(
                name=name,
                current_year=current_year,
                civilization_id=civilization_id,
                needed=100,  # this numbe will not mater
            )
            project.tile_id = tile_id
            table.insert(project.__dict__)
            return project

    def _fail(self):
        # make civtec not active
        tile = self.tile
        tile.controler_id = None
        tile.save()
        self.delete

    @property
    def tile(self):
        from db.map import Tile

        return Tile.get(self.tile_id)

    @property
    def needed(self):
        from controlpanel.costs import calculate_maintance_cost_for_tile

        return calculate_maintance_cost_for_tile(self.tile)

    @needed.setter
    def needed(self, value):
        # this is here to make sure there are no attribute errors.
        pass


class TechnologyMaintenanceProject(MaintenanceProject):
    """
    Fields:
        id                      uuid
        name                    str
        spent                   int
        last_spent              float
        needed                  int
        civilization_id         uuid
        maintenance_window      float
        last_maintained         float
        technology_id           uuid
            Points to civtec
    """

    @classmethod
    def create(
        cls,
        current_year,
        civilization_id,
        civ_tech,
        name=None,
    ):
        with get_db() as db:
            table = db.table(Project.TABLE_NAME)

            if not name:
                name = ("Maintaince for " + civ_tech.technology.name,)

            project = super(TechnologyMaintenanceProject, cls).create(
                name=name,
                current_year=current_year,
                needed=civ_tech.needed_maintenance,
                civilization_id=civilization_id,
            )
            project.technology_id = civ_tech.id
            table.insert(project.__dict__)
            return project

    def _fail(self):
        # make civtec not active
        tec = self.technology
        tec.active = False
        tec.save()

        # to should project staty around after it fails?

    def _complete(self, year):
        tec = self.technology
        tec.active = True
        tec.save()

        self.reset_maintance(year)

    def technology(self):
        from db.technology import CivTec

        return CivTec.get(self.technology_id)
