from django.db import models


class Civilization(models.Model):
    name = models.CharField(max_length=100)
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    last_year_updated = models.FloatField()

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
            year=str(int(self.last_year_updated)),season=season)

    def __str__(self):
        return self.name

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
        related_name="tiles",
        on_delete=models.SET_NULL)
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
    snowy = models.BooleanField(default=False)

    class Meta:
        unique_together = ('x', 'y', 'z')

    def __str__(self):
        if self.controler is None:
            owner = "Unoccupied"
        else:
            owner = self.controler.name

        return "{owner}: ({x}, {y}, {z})".format(
            owner=owner, x=self.x, y=self.y, z=self.z)

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
        # Todo add the others
        return assets

    def distance_between(self, other):
        return (abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)) / 2

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

        return "{name}: ({owner})".format(
            name=self.name, owner=owner)


