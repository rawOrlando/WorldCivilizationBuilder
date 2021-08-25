from db.technology import Technology, CivTec
from db.civilization import Civilization
from tests import WCBTestCase


class TestTechnology(WCBTestCase):
    def test_get_created_tile(self):
        tec = Technology.create(
            name="Test",
            tech_type="Technology",
            description="test",
        )
        got_tec = Technology.get(_id=tec.id)

        # check that they are the same.
        self.assertEqual(tec.id, got_tec.id)
        self.assertEqual(tec.name, got_tec.name)
        self.assertEqual(tec.tech_type, got_tec.tech_type)
        self.assertEqual(tec.description, got_tec.description)
        self.assertEqual(tec.prerequisite, got_tec.prerequisite)
        self.assertEqual(tec.needed_maintance, got_tec.needed_maintance)

        # clean up
        tec.delete()


class TestCivTec(WCBTestCase):
    def test_get_created_tile(self):
        civ = Civilization.create(name="Temp test")
        tec = CivTec.create(
            technology_id=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            civilization_id=civ.id,
        )
        got_tec = CivTec.get(_id=tec.id)

        # check that they are the same.
        self.assertEqual(tec.id, got_tec.id)
        self.assertEqual(tec.technology_id, got_tec.technology_id)
        self.assertEqual(tec.civilization_id, got_tec.civilization_id)

        # clean up
        tec.delete()
