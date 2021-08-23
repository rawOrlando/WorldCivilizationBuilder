import unittest
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
        super(WCBTestCase, cls).tearDownClass()

    def setUp(self):
        super(WCBTestCase, self).setUp()
        # Init your obj Mock/Patch
        my_patch = patch("db.helper.DB_PATH", new_callable=test_db_path)
        my_patch.start()
        self.addCleanup(my_patch.stop)

    # @classmethod
    # def tearDown(self):
    #     super(WCBTestCase, self).tearDown()
