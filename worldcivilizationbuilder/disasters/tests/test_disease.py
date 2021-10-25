from tests import WCBTestCase

from db.civilization import Civilization, Settlement
from db.disaster import Disaster, CurrentDisaster
from db.setup import create_base_disaster_data

from disasters.disease import suffer_disease


class TestDisease(WCBTestCase):
    def test_disease_kills_people(self):
        # this test is not running for some reason.
        civ = Civilization.create(name="Temp civ")
        # todo add locations
        settlement = Settlement.create(
            name="place", civilization_id=civ.id, location_id=None, population=10
        )

        from mock import patch

        with patch("random.randrange", return_value=1):
            suffer_disease(civ)

        settlement = Settlement.get(_id=settlement.id)

        self.assertLess(settlement.population, 10)

        # clean up
        civ.delete()
        settlement.delete()
