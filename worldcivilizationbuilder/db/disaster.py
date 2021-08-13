from tinydb import Query
from db.base import Base_DB_Model
from db.helper import Dict2Class, get_db

class Disaster(Base_DB_Model):
	""" 
    Fields:
    	id 						uuid
        name                    str
        level                   int

    """
    TABLE_NAME = 'disaster'

    # default values
    def _set_defaults(self):
        self._set_default("level", 1)
        super(Technology, self)._set_defaults()

    @staticmethod
    def create(name,
               level=1):
        with get_db() as db:
            table = db.table(Disaster.TABLE_NAME)

            disaster = Disaster()
            disaster.name = name
            disaster.level = level
            disaster._set_deafualts()
            table.insert(disaster.__dict__)
            return disaster

    @classmethod
    def get(cls, _id=None, name=None,):
        if not _id is None:
            return super(Disaster, cls).get(_id=_id, db=db)
        with get_db() as db:
            table = db.table(cls.TABLE_NAME)

            query = Query()
            values = table.get((query.name == name))

            if values:
                got = cls()
                attr_dict = values
                for key in attr_dict:
                    setattr(got, key, attr_dict[key])
                return got
            else:
                return None

    def __str__(self):
        return self.name

    @staticmethod
    def DISEASE_OUTBREAK():
        return Disaster.get(name="Disease Outbreak")

    @staticmethod
    def DRAUGHT():
        return Disaster.get(name="Draught")

    @staticmethod
    def FOREST_FIRE():
        return Disaster.get(name="Forest Fire")

    @staticmethod
    def IN_FIGHTING():
        return Disaster.get(name="In Fighting")

    @staticmethod
    def UNTIMELY_DEATH():
        return Disaster.get(name="Untimely Death")


