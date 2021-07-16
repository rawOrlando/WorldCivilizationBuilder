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

