import random
from db.technology import Technology


def suffer_disease(civilization):
    # todo rework
    # 5% chance by default
    # + 0.0(population)
    # if chance happens that person dies.
    # to make this work it will be out of 10,000
    chance = 500
    for settlement in civilization.settlements():
        population = settlement.population
        settlement_chance = chance + population
        if civilization.has_technology(Technology.SOAP_NAME):
            settlement_chance = settlement_chance // 4
        for person in range(1, population):
            happened = random.randrange(1, 10001)
            if happened <= settlement_chance:
                settlement.population -= 1

        settlement.save()
