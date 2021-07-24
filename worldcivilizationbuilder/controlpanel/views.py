from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from controlpanel.models import (Civilization,
                                 Tile, 
                                 Settlement, 
                                 Project)
from controlpanel.advance import (spend_resources,
                                  advance_civilization_a_season)
from controlpanel.costs import (get_maintance_projects,
                               generate_resources,
                               calculate_maintance_cost_for_tile)

def index(request):
    civilization_list = Civilization.objects.all()
    context = {
        'civilization_list': civilization_list,
    }
    return render(request, 'civilization_list.html', context)


def civilization(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    year = civilization.last_year_updated
    if request.POST:
        spend_resources(civilization, year=year,
            resources_spent=convert_input_to_resources_spent(request.POST))
        advance_civilization_a_season(civilization)
    
    context = {
        'civilization': civilization,
        'resources': generate_resources(civilization),
        'maintance_projects': get_maintance_projects(civilization),
        'projects': list(civilization.projects.values())
    }
    return render(request, 'civilization.html', context)


def civilization_details(request,civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    context = {
        'civilization': civilization,
        'technologies': list(civilization.technologies.all()),
        'projects': list(civilization.projects.values())
    }
    return render(request, 'civilization_details.html', context)

def new_project(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    context = {
        'civilization': civilization
    }
    return render(request, 'new_project.html', context)

def new_research(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    # Todo change this so that category is a spin choser.
    if request.POST:
        tec_name = request.POST["technology_category"]
        Project.objects.create(
            name="Research " + tec_name,
            tecnology=tec_name,
            last_spent=civilization.last_year_updated,
            civilization=civilization)
        return redirect('/'+str(civilization_id)+'/')


    context = {
        'civilization': civilization
    }
    return render(request, 'new_research.html', context)


def new_settlement(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    if request.POST:
        tile_id = request.POST["tile"].replace("tile_", "")
        name = request.POST["name"]
        settlement = Settlement.objects.create(
            name=name,
            population=0,
            civilization=civilization,
            location=Tile.objects.get(id=tile_id),
            )
        Project.objects.create(
            name="Building " + name,
            building=settlement,
            needed=30,
            last_spent=civilization.last_year_updated,
            civilization=civilization)

        return redirect('/'+str(civilization_id)+'/')
    # Get all tiles without settlements
    tiles = civilization.tiles.filter(settlements=None)
    tiles_info = []
    for tile in tiles:
        tiles_info.append(
            {
                "id": tile.id,
                "name": str(tile),
                "assets": tile.assets,
            }
        )

    context = {
        'civilization': civilization, 
        'tiles': tiles_info,
    }
    return render(request, 'new_settlement.html', context)


def new_exploration(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    if request.POST:
        tile_id = request.POST["tile"].replace("tile_", "")
        tile = Tile.objects.get(id=tile_id)
        Project.objects.create(
            name="Exploring " + str(tile),
            territory=tile,
            needed=calculate_maintance_cost_for_tile(tile),
            last_spent=civilization.last_year_updated,
            civilization=civilization)
        
        return redirect('/'+str(civilization_id)+'/')
    # Get all the tiles around your tiles.
    # Todo not right Tile
    tiles = civilization.tiles.filter(settlements=None)
    tiles_info = []
    settlement_locations = civilization.settlements.all().values_list("location", flat=True).distinct()
    for tile in tiles:
        cost = calculate_maintance_cost_for_tile(tile, settlement_locations)
        tiles_info.append(
            {
                "id": tile.id,
                "name": str(tile),
                "assets": tile.assets,
                "cost": cost,
            }
        )

    context = {
        'civilization': civilization, 
        'tiles': tiles_info,
    }
    return render(request, 'new_settlement.html', context)


def convert_input_to_resources_spent(data):
    resources_spent = []
    for key in data:
        if "maintance_" in key:
            shorten_key = key.replace("maintance_", "")
            if "tile_" in shorten_key:
                tile_id = shorten_key.replace("tile_", "")
                tile = Tile.objects.get(id=tile_id)
                resources_spent.append({
                    "type": "maintance_tile",
                    "spent_on": tile,
                    "spent": int(data[key]),
                })
        if "project_" in key:
            project_id = key.replace("project_", "")
            project = Project.objects.get(id=project_id)
            resources_spent.append({
                "type": "project",
                "spent_on": project,
                "spent": int(data[key]),
            })
    return resources_spent




