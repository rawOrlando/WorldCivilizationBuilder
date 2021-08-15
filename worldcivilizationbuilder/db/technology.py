from tinydb import Query
from db.base import Base_DB_Model
from db.helper import Dict2Class, get_db


class Technology(Base_DB_Model):
    """
    Fields:
        id                      uuid
        name                    str
        tec_type                str
        description             str
        prerequisite            uuid
        needed_maintance        int

    """

    BONE_TOOLS_NAME = "Bone Tools"
    FIRE_NAME = "Fire"
    BOILING_WATER_NAME = "Boiling Water"
    COMPOSITE_TOOLS_NAME = "Composite Tools"
    TANNING_NAME = "Tanning"
    FOOD_DRYING_NAME = "Food Drying"
    DOMESTICATED_DOGS_NAME = "Domesticated Dogs"
    SOAP_NAME = "Soap"
    SLINGS_NAME = "Slings"
    PALEO_TECH_NAMES = [
        BONE_TOOLS_NAME,
        FIRE_NAME,
        BOILING_WATER_NAME,
        COMPOSITE_TOOLS_NAME,
        TANNING_NAME,
        FOOD_DRYING_NAME,
        DOMESTICATED_DOGS_NAME,
        SOAP_NAME,
        SLINGS_NAME,
    ]

    TABLE_NAME = "technology"

    # default values
    def _set_deafualts(self):
        self._set_default("prerequisite", None)
        self._set_default("needed_maintance", 0)
        super(Technology, self)._set_defaults()

    @staticmethod
    def create(name, tech_type, description, prerequisite=None, needed_maintance=0):
        with get_db() as db:
            table = db.table(Technology.TABLE_NAME)

            technology = Technology()
            technology.name = name
            technology.tech_type = tech_type
            technology.description = description
            technology.prerequisite = prerequisite
            technology.needed_maintance = needed_maintance
            technology._set_deafualts()
            table.insert(technology.__dict__)
            return technology


class CivTec(Base_DB_Model):
    """
    Fields:
        id                      uuid
        technology_id           uuid
        civilization_id         uuid
        active                  boolean

    """

    TABLE_NAME = "civilization_technology"

    # default values
    def _set_deafualts(self):
        self._set_default("active", True)
        super(CivTec, self)._set_defaults()

    @staticmethod
    def create(
        technology_id,
        civilization_id,
        active=False,
    ):
        with get_db() as db:
            table = db.table(CivTec.TABLE_NAME)

            civ_tec = CivTec()
            civ_tec.technology_id = technology_id
            civ_tec.civilization_id = civilization_id
            civ_tec.active = active
            civ_tec._set_deafualts()
            table.insert(civ_tec.__dict__)
            return civ_tec

    @property
    def needed_maintenance(self):
        return self.technology.needed_maintance

    @property
    def technology(self):
        return Technology.get(self.technology_id)
