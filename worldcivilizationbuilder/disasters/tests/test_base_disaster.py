from tests import WCBTestCase

from db.civilization import Civilization, Settlement
from db.disaster import Disaster, CurrentDisaster

from disasters.disaster import (
    is_in_a_draught,
    during_forest_fire,
    is_in_fighting,
    durring_epidemic,
)


class TestBasicDisater(WCBTestCase):
    def test_not_current_disaster(self):
        civ = Civilization.create(name="Temp civ")

        # All should be false are false when
        self.assertFalse(is_in_a_draught(civ))
        self.assertFalse(during_forest_fire(civ))
        self.assertFalse(is_in_fighting(civ))
        self.assertFalse(durring_epidemic(civ))

        # clean up
        civ.delete()

    def test_in_a_draught(self):
        civ = Civilization.create(name="Temp civ")

        cur_dis = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.DRAUGHT().id,
            start_time=0,
            end_time=1,
        )

        self.assertTrue(is_in_a_draught(civ))

        # clean up
        civ.delete()
        cur_dis.delete()

    def test_during_forest_fure(self):
        civ = Civilization.create(name="Temp civ")

        cur_dis = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.FOREST_FIRE().id,
            start_time=0,
            end_time=1,
        )

        self.assertTrue(during_forest_fire(civ))

        # clean up
        civ.delete()
        cur_dis.delete()

    def test_is_in_fighting(self):
        civ = Civilization.create(name="Temp civ")

        cur_dis = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.IN_FIGHTING().id,
            start_time=0,
            end_time=1,
        )

        self.assertTrue(is_in_fighting(civ))

        # clean up
        civ.delete()
        cur_dis.delete()

    def test_durring_epidemic(self):
        civ = Civilization.create(name="Temp civ")

        cur_dis = CurrentDisaster.create(
            civilization_id=civ.id,
            disaster_id=Disaster.DISEASE_OUTBREAK().id,
            start_time=0,
            end_time=1,
        )

        self.assertTrue(durring_epidemic(civ))

        # clean up
        civ.delete()
        cur_dis.delete()
