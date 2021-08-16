from tinydb.database import TinyDB
import os


def test_db_path():
    return os.getcwd() + "/test-db.json"
