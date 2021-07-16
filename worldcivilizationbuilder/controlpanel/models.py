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