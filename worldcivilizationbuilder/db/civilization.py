from db.base import Base_DB_Model, get_db
#from db.projects import Project

class Civilization(Base_DB_Model):
    """ 
    Fields:
        id                      uuid
        name                    str
        last_year_updated       float
        technologies_ids        list uuid to civtec

    """
    TABLE_NAME = 'civilization'

    def __str__(self):
        return self.name

    # default values
    def _set_defaults(self):
        self._set_default("last_year_updated", 0)
        self._set_default("technologies_ids", [])
        super(Civilization, self)._set_defaults()


    @staticmethod
    def create(name, last_year_updated=0):
        with get_db() as db:
            table = db.table(Civilization.TABLE_NAME)

            civilization = Civilization()
            civilization.name = name
            civilization.last_year_updated = last_year_updated
            civilization._set_defaults()
            table.insert(civilization.__dict__)
            return civilization

    def territories(self):
        from db.map import Tile
        return Tile.filter((Query().controler_id == self.id))

    def technologies(self):
        # todo utilize technologies_ids
        from db.technology import CivTec
        return CivTec.filter((query.civilization_id == self.id))

    def settlements(self):
        return Settlement.filter((Query().civilization_id == self.id))

    def get_all_settlement_locations(self):
        # todo this feels make sure locations are unique.
        return [settlement.location for settlement in self.settlements]

    def can_hunt(self):
        from db.technology import Technology
        return (self.has_technology(Technology.BONE_TOOLS_NAME) or
            self.has_technology(Technology.SLINGS_NAME))

    def can_spear_fish(self):
        from db.technology import Technology
        return self.has_technology(Technology.BONE_TOOLS_NAME)

    def has_technology(self, technology_name):
        # todo maybe we could short circuit this.
        # todo split this to muliple lines
        return bool([civtec for civtec in self.technologies if civtec.active and civtec.technology.name == technology_name])

    def has_technology_knowledge(self, technology_name):
        # todo maybe we could short circuit this.
        # todo split this to muliple lines
        return bool([civtec for civtec in self.technologies if civtec.active and civtec.technology.name == technology_name])

    def possible_exploration_tiles(self):
        pass 
        # todo


class Settlement(Base_DB_Model):
    """ 
    Fields:
        id                      uuid
        name                    str
        population              int
        is_capital              boolean
        civilization_id         uuid
        location_id             uuid

    """
    TABLE_NAME = 'settlement'

    # default values
    def _set_defaults(self):
        self._set_default("is_capital", False)
        self._set_default("population", 0)
        super(Settlement, self)._set_defaults()


    @staticmethod
    def create(name, civilization_id, location_id,
               population=0, is_capital=False):
        with get_db() as db:
            table = db.table(Settlement.TABLE_NAME)

            settlement = Settlement()
            settlement.name = name
            settlement.civilization_id = civilization_id
            settlement.location_id = location_id
            settlement.population = population
            settlement.is_capital = is_capital
            settlement._set_defaults()
            table.insert(settlement.__dict__)
            return settlement

    def civilization(self):
        return Civilization.get(self.civilization_id)

    def location(self): 
        from db.map import Tile
        return Tile.get(self.location_id)



