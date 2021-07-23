from django.contrib import admin

from controlpanel.models import (
	Civilization, 
	CivTec,
	Project, 
	Settlement, 
	Tile,
	Technology)

admin.site.register(Civilization)
admin.site.register(CivTec)
admin.site.register(Project)
admin.site.register(Settlement)
admin.site.register(Tile)
admin.site.register(Technology)
