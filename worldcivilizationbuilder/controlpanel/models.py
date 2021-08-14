from django.db import models
from django.db.models import Q


class Civilization(models.Model):
    name = models.CharField(max_length=100)
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    last_year_updated = models.FloatField()
    technologies = models.ManyToManyField("Technology", through="CivTec")

    @property
    def year_str(self):
        if self.last_year_updated % 1 == 0.0:
            season = "Spring"
        elif self.last_year_updated % 1 == 0.25:
            season = "Summer"
        elif self.last_year_updated % 1 == 0.5:
            season = "Fall"
        elif self.last_year_updated % 1 == 0.75:
            season = "Winter"
        else:
            season = "Mistake"

        return "{year} {season}".format(
            year=str(int(self.last_year_updated)), season=season
        )

    def __str__(self):
        return self.name

    def can_hunt(self):
        return self.civtec.filter(
            Q(technology__name=Technology.BONE_TOOLS_NAME, active=True)
            | Q(technology__name=Technology.SLINGS_NAME),
            active=True,
        ).exists()

    def can_spear_fish(self):
        return self.has_technology(Technology.BONE_TOOLS_NAME)

    def has_technology(self, technology_name):
        return self.civtec.filter(
            technology__name=technology_name, active=True
        ).exists()

    def has_technology_knowledge(self, technology_name):
        return self.civtec.filter(technology__name=technology_name).exists()

    def get_all_settlement_locations(self):
        return (
            self.settlements.filter(projects=None)
            .values_list("location", flat=True)
            .distinct()
        )

    def possible_exploration_tiles(self):
        # Get all the tiles around your tiles.
        # todo find a way to do this with django
        neighbors = set()
        # for now need rivers
        for controled_tile in self.tiles.all():
            neighbors = neighbors.union(set(controled_tile.get_neighbors()))

        neighbors = neighbors.difference(list(self.tiles.all()))

        for tile in neighbors.copy():
            if (
                not tile.river
                # Todo cleaner way?
                and not (
                    self.has_technology(Technology.BOILING_WATER_NAME) and tile.shore
                )
            ):
                neighbors.remove(tile)
        return neighbors


# Todo move this stuff to a app called map
class Tile(models.Model):
    # https://www.redblobgames.com/grids/hexagons/#coordinates
    # x + y + z = 0
    # North(+y,-z) to South(-y,+z),
    x = models.IntegerField()
    # North East(+x,-z) to South West(-x,+z)
    y = models.IntegerField()
    # North West(+x,-y) to South East(-x,+y)
    z = models.IntegerField()

    controler = models.ForeignKey(
        Civilization,
        null=True,
        blank=True,
        related_name="tiles",
        on_delete=models.SET_NULL,
    )
    # Assets on the tile
    forest = models.BooleanField(default=False)
    tropical_forest = models.BooleanField(default=False)
    desert = models.BooleanField(default=False)
    hills = models.BooleanField(default=False)
    mountain = models.BooleanField(default=False)
    plains = models.BooleanField(default=False)
    river = models.BooleanField(default=False)
    lake = models.BooleanField(default=False)
    shore = models.BooleanField(default=False)
    ocean = models.BooleanField(default=False)
    snowy = models.BooleanField(default=False)

    # The stuf fpr maintance
    # Maybe should be moved.
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    last_year_updated = models.FloatField(default=0)
    # Spent so far this year
    maintance_spent_already = models.IntegerField(default=0)
    maintaned = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "x",
            "y",
            "z",
        )

    def __str__(self):
        if self.controler is None:
            owner = "Unoccupied"
        else:
            owner = self.controler.name

        return "{owner}: ({x}, {y}, {z})".format(
            owner=owner, x=self.x, y=self.y, z=self.z
        )

    @property
    def owner(self):
        if self.controler is None:
            return "Unoccupied"
        return self.controler.name

    @property
    def assets(self):
        assets = []
        if self.forest:
            assets.append("Forest")
        if self.tropical_forest:
            assets.append("Tropical Forest")
        if self.river:
            assets.append("River")
        if self.shore:
            assets.append("Shore")
        if self.plains:
            assets.append("Plains")
        if self.hills:
            assets.append("Hill")
        # Todo add the others
        return assets

    def reset_maintance(self):
        self.maintaned = False
        self.maintance_spent_already = 0

    def distance_between(self, other):
        return (
            abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
        ) / 2

    def get_neighbors(self):
        # Todo: Make this more django
        # North +y, -z
        north, created = Tile.objects.get_or_create(
            x=self.x, y=self.y + 1, z=self.z - 1
        )
        # North East +x, -z
        north_east, created = Tile.objects.get_or_create(
            x=self.x + 1, y=self.y, z=self.z - 1
        )
        # South East +x, -y
        south_east, created = Tile.objects.get_or_create(
            x=self.x + 1, y=self.y - 1, z=self.z
        )
        # South -y, +z
        south, created = Tile.objects.get_or_create(
            x=self.x, y=self.y - 1, z=self.z + 1
        )
        # North West -x, +z
        north_west, created = Tile.objects.get_or_create(
            x=self.x - 1, y=self.y, z=self.z + 1
        )
        # South West -x, +y
        south_west, created = Tile.objects.get_or_create(
            x=self.x - 1, y=self.y + 1, z=self.z
        )

        return {north, north_east, north_west, south, south_east, south_west}

    @property
    def being_claimed(self):
        if self.projects.exists():
            return True
        return False


class Settlement(models.Model):
    name = models.CharField(max_length=100)
    population = models.IntegerField()
    is_capital = models.BooleanField(default=False)
    civilization = models.ForeignKey(
        Civilization,
        related_name="settlements",
        on_delete=models.PROTECT,
    )
    location = models.ForeignKey(
        Tile,
        related_name="settlements",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        if self.civilization is None:
            owner = "Unoccupied"
        else:
            owner = self.civilization.name

        return "{name}: ({owner})".format(name=self.name, owner=owner)

    @property
    def being_built(self):
        if self.projects.exists():
            return True
        return False


class Technology(models.Model):
    BONE_TOOLS_NAME = "Bone Tools"
    FIRE_NAME = "Fire"
    BOILING_WATER_NAME = "Boiling Water"
    COMPOSITE_TOOLS_NAME = "Composite Tools"
    TANNING_NAME = "Tanning"
    FOOD_DRYING_NAME = "Food Drying"
    DOMESTICATED_DOGS_NAME = "Domesticated Dogs"
    SOAP_NAME = "Soap"
    SLINGS_NAME = "Slings"
    PALEO_TECH_NAMES = [
        BONE_TOOLS_NAME,
        FIRE_NAME,
        BOILING_WATER_NAME,
        COMPOSITE_TOOLS_NAME,
        TANNING_NAME,
        FOOD_DRYING_NAME,
        DOMESTICATED_DOGS_NAME,
        SOAP_NAME,
        SLINGS_NAME,
    ]

    name = models.CharField(max_length=100)
    tec_type = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    prerequisite = models.ForeignKey(
        "Technology",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="unlocks",
    )
    needed_maintance = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CivTec(models.Model):
    # todo rename this...?
    civilization = models.ForeignKey(
        "Civilization", on_delete=models.CASCADE, related_name="civtec"
    )
    technology = models.ForeignKey("Technology", on_delete=models.CASCADE)
    # The stuff for maintance
    # Maybe should be moved.
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    last_year_maintance_applied = models.FloatField(default=0)
    # Spent so far this year
    maintance_spent_already = models.IntegerField(default=0)
    # Should this field only
    needed_maintance = models.IntegerField()
    maintaned = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    @property
    def needed_maintance(self):
        if self.technology.needed_maintance:
            return self.technology.needed_maintance
        return 0

    def reset_maintance(self):
        self.maintaned = False
        self.maintance_spent_already = 0
