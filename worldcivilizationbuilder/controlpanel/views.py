from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from controlpanel.models import Civilization
from controlpanel.costs import (get_maintance_projects,
                               generate_resources)

def index(request):
    civilization_list = Civilization.objects.all()
    context = {
        'civilization_list': civilization_list,
    }
    return render(request, 'civilization_list.html', context)


def civilization(request, civilzation_id):
    civilization = Civilization.objects.get(id=civilzation_id)
    context = {
        'civilization': civilization,
        'resources': generate_resources(civilization),
        'maintance_projects': get_maintance_projects(civilization),
        'projects': list(civilization.projects.values())
    }
    return render(request, 'civilization.html', context)




