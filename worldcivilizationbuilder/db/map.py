from tinydb import Query
from db.base import Base_DB_Model
from db.helper import Dict2Class, get_db

class Tile(Base_DB_Model):
    """ 
    Fields:
        id                      uuid
        x                       int
        y                       int
        z                       int
        controler_id            uuid
        resources               list str

    """
    TABLE_NAME = 'tile'
    # https://www.redblobgames.com/grids/hexagons/#coordinates
    # x + y + z = 0
    # North(+y,-z) to South(-y,+z), 
    # should have x as an int
    # North East(+x,-z) to South West(-x,+z)
    # should have y as an int
    # North West(+x,-y) to South East(-x,+y)
    # should have z as an int

    # default values
    def _set_defaults(self):
        self._set_default("controler_id", None)
        self._set_default("resources", [])
        super(Tile, self)._set_defaults()

    @staticmethod
    def create(x, y, z, 
               controler_id=None, resources=[],):
        with get_db() as db:
            table = db.table(Tile.TABLE_NAME)

            # todo enforce unique x, y, z  ??

            tile = Tile()
            tile.x = x
            tile.y = y
            tile.z = z
            tile.controler_id = controler_id
            tile.resources = resources
            tile._set_defaults()
            table.insert(tile.__dict__)
            return tile

    @staticmethod
    def get_or_create(x, y, z,):
        with get_db() as db:
            # Get 
            tile = Tile.get(x=x, y=y, z=z, db=db)
            if tile is None:
                # Create
                tile = Tile.create(x=x, y=y, z=z, db=db)

            return tile

    @classmethod
    def get(cls, _id=None, x=None, y=None, z=None, db=None,):
        if not _id is None:
            return super(Tile, cls).get(_id=_id, db=db)
        if not db:
            db = get_db()
        table = db.table(cls.TABLE_NAME)

        # require x, y, and z
        query = Query()
        values = table.get((query.x == x) & (query.y == y) & (query.z == z))

        if values:
            got = cls()
            attr_dict = values
            for key in attr_dict:
                setattr(got, key, attr_dict[key])
            return got
        else:
            return None


    def __str__(self):
        controler = self.controler
        if controler  is None:
            owner = "Unoccupied"
        else:
            owner = controler.name

        return "{owner}: ({x}, {y}, {z})".format(
            owner=owner, x=self.x, y=self.y, z=self.z)

    def controler(self):
        if not self.controler_id:
            return None
        from db.civilization import Civilization
        return Civilization.get(self.controler_id)



