from db.civilization import Civilization, Settlement
from db.map import Tile
from db.disaster import Disaster
from db.technology import Technology
from controlpanel.models import Civilization as OldCivilization
from controlpanel.models import Tile as OldTile
from controlpanel.models import Settlement as OldSettlement
from disaster.models import Disaster as OldDisaster
from controlpanel.models import Technology as OldTechnology


def copy_old_data():

    for old_tile in OldTile.objects.all():
        Tile.create(x=old_tile.x, y=old_tile.y, z=old_tile.z, assets=old_tile.assets)

    for old_civilization in OldCivilization.objects.all():
        civ = Civilization.create(
            name=old_civilization.name,
            last_year_updated=old_civilization.last_year_updated,
        )
        for old_tile in old_civilization.tiles:
            tile = Tile.get(x=old_tile.x, y=old_tile.y, z=old_tile.z)
            tile.controler_id = civ.id
            tile.save()

        for old_settlement in old_civilization.settlements:
            old_tile = old_settlement.location
            tile = tile = Tile.get(x=old_tile.x, y=old_tile.y, z=old_tile.z)
            Settlement.create(
                name=old_settlement.name,
                civilization_id=civ.id,
                location_id=tile.id,
                is_capital=old_settlement.is_capital,
                population=old_settlement.population,
            )

    for old_disaster in OldDisaster.objects.all():
        Disaster.create(name=old_disaster.name, level=old_disaster.level)

    for old_technology in OldTechnology.objects.all():
        Technology.create(
            name=old_technology.name,
            tech_type=old_technology.tech_type,
            description=old_technology.description,
            needed_maintance=old_technology.needed_maintance,
            prerequisite=None,
        )
        # how do we deal with prerequisite


if __name__ == "__main__":
    copy_old_data()
