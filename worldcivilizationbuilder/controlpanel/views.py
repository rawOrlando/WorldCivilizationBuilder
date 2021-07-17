from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from controlpanel.models import Civilization
form controlpanel.cost import generate_resources

def index(request):
    civilization_list = Civilization.objects.all()
    template = loader.get_template('civilization_list.html')
    context = {
        'civilization_list': civilization_list,
    }

    return HttpResponse(template.render(context, request))


def civilization(request, civilzation_id):
    civ = Civilization.objects.get(id=civilzation_id)
    return HttpResponse("{name}: {resources}".format(
            name=civ.name, resources=str(generate_resources(civ))))




