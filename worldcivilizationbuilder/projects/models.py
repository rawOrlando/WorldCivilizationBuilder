from django.db import models
from controlpanel.models import Civilization, Settlement, Technology, Tile

from controlpanel.population import migrate_initial_population_to_new_settlement
from technology import unlock_another_technology

import random


class ProjectOption(models.IntegerChoices):
    research = (1, "Research Project")
    exploration = (2, "Exploration Project")
    settlement = (3, "Found Settlement Project")
    region_maintance = (4, "Region Maintance")
    technology_maintance = (5, "Technology Maintance")


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

    project_type = models.IntegerField(choices=ProjectOption.choices)
    specific_project_id = models.IntegerField()

    @property
    def specfic_project(self):
        # replace with a switch
        if self.project_type == ProjectOption.research:
            return ResearchProject.objects.get(id=self.specific_project_id)
        elif self.project_type == ProjectOption.exploration:
            return ExplorationProject.objects.get(id=self.specific_project_id)
        elif self.project_type == ProjectOption.settlement:
            return SettlementProject.objects.get(id=self.specific_project_id)
        elif self.project_type == ProjectOption.region_maintance:
            return TileMaintanceProject.objects.get(id=self.specific_project_id)
        elif self.project_type == ProjectOption.technology_maintance:
            return TechnologyMaintanceProject.objects.get(id=self.specific_project_id)
        # Todo this should not be possible
        return None

    def delete(self, *args, **kwargs):
        self.specfic_project.delete(*args, **kwargs)
        super(Project, self).delete(*args, **kwargs)

    def spend(self, amount):
        self.spent += amount
        self.last_spent = self.civilization.last_year_updated

        if self._is_complete():
            self.specfic_project._complete()
            self.delete()
            return

        self.save()

    def _is_complete(self):
        if self.project_type == ProjectOption.research:
            return self.specfic_project._is_complete()
        return self.spent >= self.needed

    def __str__(self):
        return "{name}: ({owner})".format(name=self.name, owner=self.civilization.name)


class SpecficProject(models.Model):
    """
    This is some stuff for all  general the specfic project models
    to simply to the the relation ship
    """

    # type should be set in base class
    TYPE = None

    base_project = tile = models.ForeignKey(
        Project,
        null=True,
        default=None,
        # unique=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __getattr__(self, item):
        # Band aid __dict__ has civilization_id not civilization
        if item == "civilization":
            return self.base_project.civilization
        if item in self.base_project.__dict__:
            return self.base_project.__dict__[item]
        raise AttributeError(
            "%r object has no attribute %r" % (self.__class__.__name__, item)
        )

    @classmethod
    def _create_project(cls, name, last_spent, civilization, needed=None, **kwargs):

        spec_proj = cls.objects.create(**kwargs)

        print(spec_proj.id)

        spec_proj.base_project = Project.objects.create(
            name=name,
            needed=needed,
            last_spent=last_spent,
            civilization=civilization,
            project_type=spec_proj.TYPE,
            specific_project_id=spec_proj.id,
        )

        spec_proj.save()

    def __str__(self):
        return self.base_project.__str__()


class ResearchProject(SpecficProject):
    TYPE = ProjectOption.research

    technology_type = models.CharField(
        max_length=100,
    )

    def _is_complete(self):
        chance = random.randrange(1, 101)
        return self.base_project.spent >= chance

    def _complete(self):
        unlock_another_technology(self.civilization)


class ExplorationProject(SpecficProject):
    TYPE = ProjectOption.exploration

    territory = models.ForeignKey(
        Tile,
        related_name="projects",
        on_delete=models.CASCADE,
    )

    def _complete(self):
        self.territory.controler = self.civilization
        self.territory.last_year_updated = self.civilization.last_year_updated
        self.territory.maintaned = True
        self.territory.save()


class SettlementProject(SpecficProject):
    TYPE = ProjectOption.settlement

    settlement = models.ForeignKey(
        Settlement,
        related_name="projects",
        on_delete=models.CASCADE,
    )

    def delete(self, *args, **kwargs):
        if not self.base_project._is_complete():
            self.settlement.delete()
        super(SettlementProject, self).delete(*args, **kwargs)

    def _complete(self):
        migrate_initial_population_to_new_settlement(self.settlement)


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
    TYPE = ProjectOption.region_maintance

    tile = models.OneToOneField(
        Tile,
        related_name="maintance_project",
        on_delete=models.CASCADE,
    )


class TechnologyMaintanceProject(Maintance, SpecficProject):
    TYPE = ProjectOption.technology_maintance

    technology = models.OneToOneField(
        Technology,
        related_name="maintance_project",
        on_delete=models.CASCADE,
    )

    @property
    def needed(self):
        # is there a better way to override the value of needed for conect Project value
        self.technology.needed_maintance
