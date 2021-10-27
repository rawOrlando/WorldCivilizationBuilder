from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newcivilization", views.new_civilization, name="new_civilization"),
    path(
        "newcivilization/land/<str:civilization_id>/",
        views.new_civilization_land,
        name="new_civilization_land",
    ),
    path(
        "newcivilization/capital/<str:civilization_id>/",
        views.new_civilization_capital,
        name="new_civilization_land",
    ),
    path("newtile", views.new_tile, name="new_tile"),
    path("<str:civilization_id>/", views.civilization, name="civilization"),
    path(
        "details/<str:civilization_id>/",
        views.civilization_details,
        name="civilization_details",
    ),
    path("newproject/<str:civilization_id>/", views.new_project, name="new_project"),
    path("newresearch/<str:civilization_id>/", views.new_research, name="new_research"),
    path(
        "newsettlement/<str:civilization_id>/",
        views.new_settlement,
        name="new_settlement",
    ),
    path(
        "newexploration/<str:civilization_id>/",
        views.new_exploration,
        name="new_exploration",
    ),
]
