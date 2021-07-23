from django.contrib import admin

from disasters.models import (
	CurrentDisaster, 
	Disaster)

admin.site.register(CurrentDisaster)
admin.site.register(Disaster)
