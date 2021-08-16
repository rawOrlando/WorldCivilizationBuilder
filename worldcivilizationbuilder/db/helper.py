from tinydb.database import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

import json
import os


DB_PATH = os.getcwd() + "/db.json"


class Dict2Class(object):
    def __init__(self, my_dict):
        print(my_dict)
        for key in my_dict:
            setattr(self, key, my_dict[key])


def get_db():
    return TinyDB(DB_PATH)  #
    # Todo figure out  this pieces, storage=CachingMiddleware(JSONStorage))


def prettify_db():
    with open(DB_PATH) as f:
        json_data = json.load(f)

    with open(DB_PATH, "w") as text_file:
        text_file.write(json.dump(json_data, indent=2))
