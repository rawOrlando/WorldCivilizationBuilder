from db.disaster import Disaster, CurrentDisaster
from disasters.disease import suffer_disease
from tinydb import Query
import random


def next_disaster(year, civilization):
    chance = random.randrange(1, 7)
    if chance == 1:
        # Disease Outbreak
        CurrentDisaster.create(
            civilization=civilization,
            disaster=Disaster.DISEASE_OUTBREAK(),
            start_time=year,
            end_time=year + 1,
        )
    elif chance == 2:
        # Imporant person died untimely.
        print("Imporant person died untimely!")
        # Todo giure out what to do her
        # erase research and lose population
        CurrentDisaster.create(
            civilization=civilization,
            disaster=Disaster.UNTIMELY_DEATH(),
            start_time=year,
            end_time=year + 1,
        )
    elif chance == 3:
        # Draught
        CurrentDisaster.create(
            civilization=civilization,
            disaster=Disaster.DRAUGHT(),
            start_time=year,
            end_time=year + 1,
        )
    elif chance == 4:
        # In Fighting
        CurrentDisaster.create(
            civilization=civilization,
            disaster=Disaster.IN_FIGHTING(),
            start_time=year,
            end_time=year + 1,
        )
    elif chance == 5:
        # Forest Fire
        CurrentDisaster.create(
            civilization=civilization,
            disaster=Disaster.FOREST_FIRE(),
            start_time=year,
            end_time=year + 1,
        )
    elif chance == 6:
        # No disaster Yeah!
        pass


def is_in_a_draught(civilization):
    return bool(
        CurrentDisaster.filter(
            (
                (Query().civilization_id == civilization.id)
                & (Query().disaster_id == Disaster.DRAUGHT().id)
            )
        )
    )


def during_forest_fire(civilization):
    return bool(
        CurrentDisaster.filter(
            (
                (Query().civilization_id == civilization.id)
                & (Query().disaster_id == Disaster.FOREST_FIRE().id)
            )
        )
    )


def is_in_fighting(civilization):
    return bool(
        CurrentDisaster.filter(
            (
                (Query().civilization_id == civilization.id)
                & (Query().disaster_id == Disaster.IN_FIGHTING().id)
            )
        )
    )


def durring_epidemic(civilization):
    return bool(
        CurrentDisaster.filter(
            (
                (Query().civilization_id == civilization.id)
                & (Query().disaster_id == Disaster.DISEASE_OUTBREAK().id)
            )
        )
    )


def move_disaster_along(disaster, new_time):
    if disaster.id == Disaster.DISEASE_OUTBREAK().id:
        suffer_disease(disaster.civilization)
    if disaster.end_time <= new_time:
        end_disater(disaster)


def end_disater(disaster):
    disaster.delete()
