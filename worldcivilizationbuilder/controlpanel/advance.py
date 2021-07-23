from controlpanel.costs import calculate_maintance_cost_for_tile
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
        civilization.settlements.all().values_list(
            "location", flat=True
        ).distinct())
    if needed <= tile.maintance_spent_already:
        tile.maintaned = True
    tile.save()

def spend_resources_on_project(project, spent, civilization, year):
    # Todo split this up
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

    civilization.last_year_updated = 0.25 + civilization.last_year_updated

    # if new year 
    if civilization.last_year_updated % 1 == 0.0:
        # Lose tiles if un maintaned
        for tile in civilization.tiles.all():
            print(tile.maintaned)
            if not tile.maintaned:
                tile.controler = None
            tile.reset_maintance()

            tile.save()

        repopulate(civilization)

        # Disaster check
        # Todo

    civilization.save()

def repopulate(civilization):
    for settlement in civilization.settlements.all():
        for i in range(-1, settlement.population % 10):
            chance = random.randrange(1,100)
            if chance <= 10:
                settlement.population += 1