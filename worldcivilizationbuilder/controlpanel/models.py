from django.db import models


class Civilization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tile(models.Model):
    colum = models.IntegerField()
    row = models.IntegerField()
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

    def __str__(self):
        if self.controler is None:
            owner = "Unoccupied"
        else:
            owner = self.controler.name

        return "{owner}: ({row}, {colum})".format(
            owner=owner, row=self.row, colum=self.colum)

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


