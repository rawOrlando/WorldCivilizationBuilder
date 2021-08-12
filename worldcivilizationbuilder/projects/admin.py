from django.contrib import admin
from projects.models import Project, ResearchProject, ExplorationProject, SettlementProject

admin.site.register(Project)
admin.site.register(ResearchProject)
admin.site.register(ExplorationProject)
admin.site.register(SettlementProject)
