from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from controlpanel.models import Civilization

def index(request):
    civilization_list = Civilization.objects.all()
    template = loader.get_template('civilization_list.html')
    context = {
        'civilization_list': civilization_list,
    }

    return HttpResponse(template.render(context, request))


def civilization(request, civilzation_id):
    civ = Civilization.objects.get(id=civilzation_id)
    #output = civ.name + " " + str(generate_resources(civ))
    generate_resources(civ)
    return HttpResponse("{name}: {resources}".format(
            name=civ.name, resources=str(generate_resources(civ))))


def generate_resources(civilzation):
    assets = {
        "Forests": 0,
        "Tropical Forests": 0,
        "Rivers": 0,
        "Shores": 0,
        "Plains": 0,
    }
    resource = 0
    for tile in civilzation.tiles.all():
        for asset in tile.assets:
            assets[asset+"s"] += 1

    # Generate food reasouces from Tropical Forests
    resource += assets["Tropical Forests"]

    # Generate food/water resources from Rivers
    resource += assets["Rivers"]

    return resource
