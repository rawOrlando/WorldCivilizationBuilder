from tinydb.database import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import os


class Dict2Class(object):
    def __init__(self, my_dict):
        print(my_dict)
        for key in my_dict:
            setattr(self, key, my_dict[key])


def get_db():
    path = os.getcwd() + "/db.json"
    # todo figure out path
    return TinyDB(path)  #
    # Todo figure out  this pieces, storage=CachingMiddleware(JSONStorage))
