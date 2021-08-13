from tinydb import Query
from db.helper import Dict2Class, get_db
import uuid

class Base_DB_Model():
    TABLE_NAME = None

    def _set_defaults(self):
        # generate uuid
        self.id = str(uuid.uuid4())

    def _set_default(self, attribute, value):
        if not hasattr(self, attribute):
            setattr(self, attribute, value)

    @classmethod
    def get(cls, _id):
        with get_db() as db:
            table = db.table(cls.TABLE_NAME)

            query = Query()
            values = table.get((query.id == _id))

            if values:
                got = cls()
                attr_dict = values
                for key in attr_dict:
                    setattr(got, key, attr_dict[key])
                return got
            else:
                return None

    def save(self):
        with get_db() as db:
            table = db.table(self.TABLE_NAME)
            table.update(self.__dict__)

    def delete(self): 
        with get_db() as db:
            table = db.table(self.TABLE_NAME)
            query = Query()
            table.remove((query.id == self.id))

    # to do make a general filter method
    @classmethod
    def filter(cls, query):
        with get_db() as db:
            table = db.table(cls.TABLE_NAME)
            values_list = table.search(query)
            _result = []
            for values in values_list:
                _result.append(cls.create_from_values(values))
            return _result

    # to do make a all method
    @classmethod
    def all(cls):
        with get_db() as db:
            table = db.table(cls.TABLE_NAME)
            values_list = table.all()
            _all = []
            for values in values_list:
                _all.append(cls.create_from_values(values))
            return _all


    @classmethod
    def create_from_values(cls, dict_values):
        created = cls()
        for key in dict_values:
            setattr(created, key, dict_values[key])
        return created
