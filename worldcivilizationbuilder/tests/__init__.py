import unittest
import os
from db.civilization import Civilization, Settlement
from mock import patch
from db.tests import test_db_path


class WCBTestCase(unittest.TestCase):
    # __metaclass__ = PatchMeta

    @classmethod
    def setUpClass(cls):
        super(WCBTestCase, cls).setUpClass()
        # Init your class Mock/Patch

    @classmethod
    def tearDownClass(cls):
        # Remove Mocks or clean your singletons

        # Delete db
        # incase anything was left behind.
        if os.path.isfile(test_db_path()):
            os.remove(test_db_path())
        super(WCBTestCase, cls).tearDownClass()

    def setUp(self):
        super(WCBTestCase, self).setUp()
        # Init your obj Mock/Patch
        my_patch = patch("db.helper.DB_PATH", new_callable=test_db_path)
        my_patch.start()
        self.addCleanup(my_patch.stop)

        from db.setup import create_base_data

        create_base_data()

    # @classmethod
    # def tearDown(self):
    #     super(WCBTestCase, self).tearDown()
