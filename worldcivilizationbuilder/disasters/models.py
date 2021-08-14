from django.db import models


class Disaster(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return self.name

    @staticmethod
    def DISEASE_OUTBREAK():
        return Disaster.objects.get(name="Disease Outbreak")

    @staticmethod
    def DRAUGHT():
        return Disaster.objects.get(name="Draught")

    @staticmethod
    def FOREST_FIRE():
        return Disaster.objects.get(name="Forest Fire")

    @staticmethod
    def IN_FIGHTING():
        return Disaster.objects.get(name="In Fighting")

    @staticmethod
    def UNTIMELY_DEATH():
        return Disaster.objects.get(name="Untimely Death")


class CurrentDisaster(models.Model):
    civilization = models.ForeignKey(
        "controlpanel.Civilization",
        on_delete=models.CASCADE,
        related_name="current_disasters",
    )
    disaster = models.ForeignKey("Disaster", on_delete=models.CASCADE)

    # The period of time for the disaster
    # .0 = Spring, .25 = Summer, .5 = Fall, .75 = Winter
    start_time = models.FloatField()
    end_time = models.FloatField()
