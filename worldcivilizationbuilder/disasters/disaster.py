from disasters.models import Disaster, CurrentDisaster
from disasters.disease import suffer_disease
import random

def next_disaster(year, civilization):
    chance = random.randrange(1,6)
    if chance == 1:
        # Disease Outbreak
        CurrentDisaster.objects.create(
            civilization=civilization,
            disaster=Disaster.DISEASE_OUTBREAK(),
            start_time=year,
            end_time=year+1,
        )
    elif chance == 2:
        # Imporant person died untimely.
        print("Imporant person died untimely!")
        # Todo giure out what to do her
        # erase research and lose population
        CurrentDisaster.objects.create(
            civilization=civilization,
            disaster=Disaster.UNTIMELY_DEATH(),
            start_time=year,
            end_time=year+1,
        )
    elif chance == 3:
        # Draught
        CurrentDisaster.objects.create(
            civilization=civilization,
            disaster=Disaster.DRAUGHT(),
            start_time=year,
            end_time=year+1,
        )
    elif chance == 4:
        # In Fighting
        CurrentDisaster.objects.create(
            civilization=civilization,
            disaster=Disaster.IN_FIGHTING(),
            start_time=year,
            end_time=year+1,
        )
    elif chance == 5:
        # Forest Fire
        CurrentDisaster.objects.create(
            civilization=civilization,
            disaster=Disaster.FOREST_FIRE(),
            start_time=year,
            end_time=year+1,
        )
    elif chance == 6:
        # No disaster Yeah!
        pass

def is_in_a_draught(civilization):
    return CurrentDisaster.objects.filter(
        civilization=civilization.id,
        disaster=Disaster.DRAUGHT()).exists()

def during_forest_fire(civilization):
    return CurrentDisaster.objects.filter(
        civilization=civilization.id,
        disaster=Disaster.FOREST_FIRE()).exists()

def is_in_fighting(civilization):
    return CurrentDisaster.objects.filter(
        civilization=civilization.id,
        disaster=Disaster.IN_FIGHTING()).exists()

def durring_epidemic(civilization):
    return CurrentDisaster.objects.filter(
        civilization=civilization.id,
        disaster=Disaster.DISEASE_OUTBREAK()).exists()



def move_disaster_along(disater, new_time):
    if disaster==Disaster.DISEASE_OUTBREAK():
        suffer_disease(disaster.civilization)
    if disaster.end_time <= new_time:
        end_disater(disaster)


def end_disater(disater):
    disaster.delete()



