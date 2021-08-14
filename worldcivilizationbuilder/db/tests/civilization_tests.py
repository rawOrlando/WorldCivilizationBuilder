import unittest
from db.civilization import Civilization, Settlement

class TestCivilization(unittest.TestCase):

    # todo test should use a seperate DB.

    def test_creation_set_values(self):
        civ = Civilization.create(name="Temp test")
        self.assertEqual(civ.name, "Temp test")

        # check default values were set
        self.assertEqual(civ.last_year_updated, 0)
        self.assertEqual(civ.technologies_ids, [])

        self.assertIsNotNone(civ.id)

        # clean up
        civ.delete()

    def test_get_created_civilization(self):
        civ = Civilization.create(name="Temp test")
        got_civ = Civilization.get(_id=civ.id)

        # check that they are the same.
        self.assertEqual(civ.id, got_civ.id)
        self.assertEqual(civ.name, got_civ.name)
        self.assertEqual(civ.last_year_updated, got_civ.last_year_updated)
        self.assertEqual(civ.technologies_ids, got_civ.technologies_ids)

        # clean up
        civ.delete()

    def test_get_civilization_that_does_not_exist(self):
        civ = Civilization.get(_id="id???")

        self.assertIsNone(civ)


class TestSettlement(unittest.TestCase):

    # todo test should use a seperate DB.

    def test_creation_set_values(self):
        civ = Civilization.create(name="Temp civ")
        # todo add locations
        settlement = Settlement.create(name = "place",
            civilization_id=civ.id, location_id=None)

        self.assertEqual(settlement.civilization_id, civ.id)
        self.assertEqual(settlement.location_id, None)
        self.assertEqual(settlement.name, "place")

        # check default values were set
        self.assertEqual(settlement.is_capital, False)
        self.assertEqual(settlement.population, 0)

        self.assertIsNotNone(settlement.id)

        # clean up
        civ.delete()
        settlement.delete()


    def test_get_created_settlement(self):
        civ = Civilization.create(name="Temp test")
        # todo add locations
        settlement = Settlement.create(name = "place",
            civilization_id=civ.id, location_id=None)
        got_settlement = Settlement.get(_id=settlement.id)

        # check that they are the same.
        self.assertEqual(settlement.id, got_settlement.id)
        self.assertEqual(settlement.civilization_id, got_settlement.civilization_id)
        self.assertEqual(settlement.location_id, got_settlement.location_id)
        self.assertEqual(settlement.name, got_settlement.name)
        self.assertEqual(settlement.is_capital, got_settlement.is_capital)
        self.assertEqual(settlement.population, got_settlement.population)

        # clean up
        civ.delete()
        settlement.delete()

if __name__ == '__main__':
    unittest.main()