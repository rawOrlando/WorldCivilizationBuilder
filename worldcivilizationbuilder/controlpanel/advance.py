from controlpanel.costs import calculate_maintance_cost_for_tile
from disasters.disaster import next_disaster
import random

def spend_resources(civilization, year, resources_spent):
    # Todo log all of this.
    for resource_spent in resources_spent:
        if resource_spent["type"] == "maintance_tile":
            spend_resources_on_tile_maintance(
                resource_spent["spent_on"],
                resource_spent["spent"],
                civilization,
                year)
        if resource_spent["type"] == "project":
            spend_resources_on_project(
                resource_spent["spent_on"],
                resource_spent["spent"],
                civilization,
                year)

def spend_resources_on_tile_maintance(tile, spent, civilization, year):
    tile.last_year_updated = year
    tile.maintance_spent_already += spent
    # Todo find a way this does not need to be calculated again
    needed = calculate_maintance_cost_for_tile(
        tile, 
        civilization.get_all_settlement_locations())
    if needed <= tile.maintance_spent_already:
        tile.maintaned = True
    tile.save()

def spend_resources_on_project(project, spent, civilization, year):
    # Todo split this up
    if not spent > 0:
        return
    project.last_spent = year
    if project.is_research():
        project.spent += spent
        project.save()
        chance = random.randrange(1,100)
        if project.spent >= chance:
            # Todo something here.
            project.delete()
            pass
    if project.is_exploration():
        project.spent += spent
        project.save()
        if project.spent >= project.needed:
            project.territory.controler = civilization
            project.territory.last_year_updated = year
            project.territory.maintaned = True
            project.territory.save()
            project.delete()
    if project.is_building_settlement():
        project.spent += spent
        project.save()
        if project.spent >= project.needed:
            # Some how get 10 population
            # project.building.project 
            project.delete()

def advance_civilization_a_season(civilization):

    new_time = 0.25 + civilization.last_year_updated
    civilization.last_year_updated = new_time

    # if new year 
    if new_time % 1 == 0.0:
        # Generate next disaster
        next_disaster(new_time, civilization)

        # Check to see if disaster repeated an escalates
        # Todo

        # Remove finished disasters
        for disaster in civilization.current_disasters.all():
            if disaster.end_time <= new_time:
                disaster.delete()

        # Lose tiles if un maintaned
        for tile in civilization.tiles.all():
            if not tile.maintaned:
                tile.controler = None
            tile.reset_maintance()

            tile.save()

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
                print(decay**2)
                project.spent -= decay**2
                project.save()

def repopulate(civilization):
    for settlement in civilization.settlements.all():
        for i in range(0, (settlement.population // 10) + 1):
            chance = random.randrange(1,100)
            if chance <= 10:
                settlement.population += 1
                settlement.save()