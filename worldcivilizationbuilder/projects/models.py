from django.db import models
from controlpanel.models import Civilization, Settlement, Technology, Tile

class Project(models.Model):
    # Claiming land, building settlements, and researching technology
    name = models.CharField(max_length=100)
    spent = models.IntegerField(default=0)
    # Last time resources were spent on this project.
    last_spent = models.FloatField()
    needed = models.IntegerField(null=True, blank=True, default=None)
    civilization = models.ForeignKey(
        Civilization,
        related_name="projects",
        on_delete=models.CASCADE,
        )

    def is_tile_maintance(self):
        return type(self.specfic_project) == TileMaintanceProject

    def is_research(self):
        return type(self.specfic_project) == ResearchProject

    def is_exploration(self):
        return type(self.specfic_project) == ExplorationProject

    def is_building_settlement(self):
        return type(self.specfic_project) == SettlementProject

    def is_technology_maintance(self):
        return type(self.specfic_project) == TechnologyMaintanceProject

    def __str__(self):
        return "{name}: ({owner})".format(
            name=self.name, owner=self.civilization.name)


class SpecficProject(models.Model):
    """
    This is some stuff for all  general the specfic project models
    to simply to the the relation ship
    """
    base_project = tile = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        )

    @property
    def name(self):
        self.base_project.name

    @property
    def spent(self):
        self.base_project.spent
    
    @property
    def last_spent(self):
        self.base_project.last_spent

    @property
    def needed(self):
        self.base_project.needed

    @property
    def civilization(self):
        self.base_project.civilization

    class Meta:
        abstract = True


class ResearchProject(SpecficProject):
    technology_type = models.CharField(
        max_length=100,)


class ExplorationProject(SpecficProject):
    territory = models.ForeignKey(
        Tile,
        related_name="projects",
        on_delete=models.CASCADE,
        )


class SettlementProject(SpecficProject):
    setlement = models.ForeignKey(
        Settlement,
        related_name="projects",
        on_delete=models.CASCADE,
        )

    def delete(self, *args, **kwargs):
        if self.building and self.needed and not self.spent >= self.needed:
            self.building.delete()
        super(SettlementProject, self).delete(*args, **kwargs)


class Maintance(models.Model):
    maintaned = models.BooleanField(default=False)

    # Made this property to stay consistent with previous stuff.
    @property
    def maintance_spent_already(self):
        return self.spent

    # Made this property to stay consistent with previous stuff.
    @property
    def last_year_updated(self):
        return self.last_spent

    def reset_maintance(self):
        self.spent = 0
        self.maintaned = False
        self.save()

    class Meta:
        abstract = True


class TileMaintanceProject(Maintance, SpecficProject):
    tile = models.OneToOneField(
        Tile,
        related_name="maintance_project",
        on_delete=models.CASCADE,
        )


class TechnologyMaintanceProject(Maintance, SpecficProject):
    technology = models.OneToOneField(
        Technology,
        related_name="maintance_project",
        on_delete=models.CASCADE,
        )
    @property
    def needed(self):
        # is there a better way to override the value of needed for conect Project value
        self.technology.needed_maintance

