from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from controlpanel.models import Civilization, Tile, Project
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


def civilization(request, civilzation_id):
    civilization = Civilization.objects.get(id=civilzation_id)
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


def convert_input_to_resources_spent(data):
    resources_spent = []
    for key in data:
        if "maintance_" in key:
            shorten_key = key.replace("maintance_", "")
            if "tile_" in shorten_key:
                tile_id = shorten_key.replace("tile_", "")
                tile = Tile.objects.get(id=tile_id)
                temp = {
                    "type": "maintance_tile",
                    "spent_on": tile,
                    "spent": int(data[key]),
                } 
                print(temp)
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




