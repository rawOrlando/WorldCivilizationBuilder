from controlpanel.costs import calculate_maintance_cost_for_tile
from controlpanel.population import (
    get_population_limit,
    migrate_initial_population_to_new_settlement,
)
from disasters.disaster import next_disaster, move_disaster_along
from controlpanel.technology import unlock_another_technology
import random


def spend_resources(civilization, year, resources_spent):
    # Todo log all of this.
    for resource_spent in resources_spent:
        if not resource_spent["spent"] > 0:
            continue
        if resource_spent["type"] == "maintance_tile":
            spend_resources_on_tile_maintance(
                resource_spent["spent_on"], resource_spent["spent"], civilization, year
            )
        elif resource_spent["type"] == "maintance_tech":
            spend_resources_on_tech_maintance(
                resource_spent["spent_on"], resource_spent["spent"], civilization, year
            )
        elif resource_spent["type"] == "project":
            resource_spent["spent_on"].spend(resource_spent["spent"])


def spend_resources_on_tile_maintance(tile, spent, civilization, year):
    tile.last_year_updated = year
    tile.maintance_spent_already += spent
    # Todo find a way this does not need to be calculated again
    needed = calculate_maintance_cost_for_tile(tile)
    if needed <= tile.maintance_spent_already:
        tile.maintaned = True
    tile.save()


def spend_resources_on_tech_maintance(tech, spent, civilization, year):
    tech.last_year_maintance_applied = year
    tech.maintance_spent_already += spent
    if tech.needed_maintance <= tech.maintance_spent_already:
        tech.maintaned = True
        tech.active = True
    tech.save()


def advance_civilization_a_season(civilization):

    new_time = 0.25 + civilization.last_year_updated
    civilization.last_year_updated = new_time

    # if new year
    if new_time % 1 == 0.0:
        # Generate next disaster
        next_disaster(new_time, civilization)

    # Remove finished disasters
    for disaster in civilization.current_disasters.all():
        move_disaster_along(disaster, new_time)

    # if new year
    if new_time % 1 == 0.0:
        # Check to see if disaster repeated an escalates
        # Todo

        # Lose tiles if un maintaned
        # for tile in civilization.tiles.all():
        #     if not tile.maintaned:
        #         tile.controler = None
        #     tile.reset_maintance()

        #     tile.save()

        # for tech in civilization.civtec.all():
        #     if tech.needed_maintance:
        #         if not tech.maintaned:
        #             tech.active = False
        #         tech.reset_maintance()

        #         tech.save()

        repopulate(civilization)

        decay_unattended_projects(civilization)

    civilization.save()


def decay_unattended_projects(civilization):
    for project in civilization.projects.all():
        decay = int(civilization.last_year_updated) - int(project.last_spent)
        if decay > 0:
            if project.spent <= 0:
                project.delete()
            else:
                project.spent -= decay ** 2
                project.save()


def repopulate(civilization):
    for settlement in civilization.settlements.all():
        if settlement.population >= get_population_limit(settlement):
            continue
        for i in range(0, (settlement.population // 10) + 1):
            chance = random.randrange(1, 101)
            if chance <= 10:
                settlement.population += 1
                settlement.save()
