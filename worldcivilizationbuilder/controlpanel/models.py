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
        blank=True,
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

    # The stuf fpr maintance
    # Maybe should be moved.
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    last_year_updated = models.FloatField(default=0)
    # Spent so far this year 
    maintance_spent_already = models.IntegerField(default=0)
    maintaned = models.BooleanField(default=False)


    class Meta:
        unique_together = ('x', 'y', 'z',)

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

    def reset_maintance(self):
        self.maintaned = False
        self.maintance_spent_already = 0

    def distance_between(self, other):
        return (abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)) / 2

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

        return "{name}: ({owner})".format(
            name=self.name, owner=owner)

    @property
    def being_built(self):
        if self.projects.exists():
            return True
        return False

class Project(models.Model):
    # Claiming land, building settlements, and researching technology
    name = models.CharField(max_length=100)
    spent = models.IntegerField()
    # Last time resources were spent on this project.
    last_spent = models.FloatField()
    needed = models.IntegerField(null=True, blank=True, default=None)
    civilization = models.ForeignKey(
        Civilization,
        related_name="projects",
        on_delete=models.CASCADE,
        )

    # Only one of these 3 should not be null
    building = models.ForeignKey(
        Settlement,
        null=True,
        default=None,
        blank=True,
        related_name="projects",
        on_delete=models.CASCADE,
        )
    territory = models.ForeignKey(
        Tile,
        null=True,
        default=None,
        blank=True,
        related_name="projects",
        on_delete=models.CASCADE,
        )
    # Todo figure out how tecnology will be done.
    tecnology = models.CharField(
        max_length=100,
        null=True,
        default=None,
        blank=True,)

    def is_research(self):
        return self.tecnology and self.territory is None and self.building is None

    def is_exploration(self):
        return self.territory and not self.tecnology and self.building is None

    def is_building_settlement(self):
        return self.building and self.territory is None and not self.tecnology

    def __str__(self):
        return "{name}: ({owner})".format(
            name=self.name, owner=self.civilization.name)

class Technology(models.Model):
    name = models.CharField(max_length=100)
    tec_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CivTec(models.Model):
    civilization = models.ForeignKey(Civilization, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    # The stuff for maintance
    # Maybe should be moved.
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    last_year_maintance_applied = models.FloatField(default=0)
    # Spent so far this year 
    maintance_spent_already = models.IntegerField(default=0)
    needed_maintance = models.IntegerField()
    maintaned = models.BooleanField(default=False)