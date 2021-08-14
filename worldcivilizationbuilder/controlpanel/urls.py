from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:civilization_id>/", views.civilization, name="civilization"),
    path(
        "details/<int:civilization_id>/",
        views.civilization_details,
        name="civilization_details",
    ),
    path("newproject/<int:civilization_id>/", views.new_project, name="new_project"),
    path("newresearch/<int:civilization_id>/", views.new_research, name="new_research"),
    path(
        "newsettlement/<int:civilization_id>/",
        views.new_settlement,
        name="new_settlement",
    ),
    path(
        "newexploration/<int:civilization_id>/",
        views.new_exploration,
        name="new_exploration",
    ),
]
