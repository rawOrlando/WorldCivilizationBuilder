from db.disaster import Disaster, CurrentDisaster
from tests import WCBTestCase
from db.setup import create_base_disaster_data
from db.civilization import Civilization


class TestDisaster(WCBTestCase):
    def test_get_created_disaster(self):
        disaster = Disaster.create(name="TEST")
        got_disaster = Disaster.get(_id=disaster.id)

        # check that they are the same.
        self.assertEqual(disaster.id, got_disaster.id)
        self.assertEqual(disaster.name, got_disaster.name)
        self.assertEqual(disaster.level, disaster.level)

        # clean up
        disaster.delete()

    def test_existance_of_disasters(self):
        self.assertIsNotNone(Disaster.DISEASE_OUTBREAK())
        self.assertIsNotNone(Disaster.DRAUGHT())
        self.assertIsNotNone(Disaster.FOREST_FIRE())
        self.assertIsNotNone(Disaster.IN_FIGHTING())
        self.assertIsNotNone(Disaster.UNTIMELY_DEATH())


class TestCurrentDisaster(WCBTestCase):
    def test_get_created_disaster(self):
        civ = Civilization.create(name="Temp test")
        c_disaster = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.DRAUGHT().id,
            start_time=10,
            end_time=12,
        )
        got_c_disaster = CurrentDisaster.get(_id=c_disaster.id)

        # check that they are the same.
        self.assertEqual(c_disaster.id, got_c_disaster.id)
        self.assertEqual(c_disaster.civilization_id, got_c_disaster.civilization_id)
        self.assertEqual(c_disaster.disaster_id, got_c_disaster.disaster_id)
        self.assertEqual(c_disaster.start_time, got_c_disaster.start_time)
        self.assertEqual(c_disaster.end_time, c_disaster.end_time)

        # clean up
        civ.delete()
        c_disaster.delete()
