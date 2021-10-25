from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from controlpanel.models import Civilization, Tile, Settlement, CivTec
from controlpanel.advance import spend_resources, advance_civilization_a_season
from controlpanel.costs import (
    get_maintance_projects,
    calculate_maintance_cost_for_tile,
    calculate_distance_to_closest_settlement,
)
from resources import acceptable_resources_spent
from projects.models import (
    Project,
    ProjectOption,
    ResearchProject,
    ExplorationProject,
    SettlementProject,
)
from resources.generate import generate_resources


def index(request):
    civilization_list = Civilization.objects.all()
    context = {
        "civilization_list": civilization_list,
    }
    return render(request, "civilization_list.html", context)


def civilization(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    year = civilization.last_year_updated
    resource_bundle = generate_resources(civilization)
    error = None
    if request.POST:
        resources_spent = convert_input_to_resources_spent(request.POST)
        # Check to make sure resources spent is corect?
        if not acceptable_resources_spent(resource_bundle, resources_spent):
            # todo have error to tell user why input was not accepted.
            error = "You spent more than was available."

        if not error:
            spend_resources(civilization, year=year, resources_spent=resources_spent)
            advance_civilization_a_season(civilization)

    context = {
        "civilization": civilization,
        "resources": resource_bundle.__dict__,
        "total_resources": resource_bundle.simmple_total(),
        "maintance_projects": get_maintance_projects(civilization),
        "projects": list(civilization.projects.values()),
        "error": error,
    }
    return render(request, "civilization.html", context)


def civilization_details(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    context = {
        "civilization": civilization,
        "technologies": list(civilization.technologies.all()),
        "projects": list(civilization.projects.values()),
    }
    return render(request, "civilization_details.html", context)


def new_project(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    context = {"civilization": civilization}
    return render(request, "new_project.html", context)


def new_research(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    # Todo change this so that category is a spin choser.
    if request.POST:
        tec_name = request.POST["technology_category"]
        ResearchProject._create_project(
            technology_type=tec_name,
            name="Research " + tec_name,
            last_spent=civilization.last_year_updated,
            civilization=civilization,
        )
        return redirect("/" + str(civilization_id) + "/")

    context = {"civilization": civilization}
    return render(request, "new_research.html", context)


def new_settlement(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    if request.POST:
        tile_id = request.POST["tile"].replace("tile_", "")
        name = request.POST["name"]
        settlement = Settlement.objects.create(
            name=name,
            population=0,
            civilization=civilization,
            location=Tile.objects.get(id=tile_id),
        )
        SettlementProject._create_project(
            name="Building " + name,
            needed=30,
            last_spent=civilization.last_year_updated,
            civilization=civilization,
            settlement=settlement,
        )

        return redirect("/" + str(civilization_id) + "/")
    # Get all tiles without settlements
    tiles = civilization.tiles.filter(settlements=None)
    tiles_info = []
    for tile in tiles:
        tiles_info.append(
            {
                "id": tile.id,
                "name": str(tile),
                "assets": tile.assets,
            }
        )

    context = {
        "civilization": civilization,
        "tiles": tiles_info,
    }
    return render(request, "new_settlement.html", context)


def new_exploration(request, civilization_id):
    civilization = Civilization.objects.get(id=civilization_id)
    settlement_locations = (
        civilization.settlements.all().values_list("location", flat=True).distinct()
    )
    if request.POST:
        tile_id = request.POST["tile"].replace("tile_", "")
        tile = Tile.objects.get(id=tile_id)
        # calulate distance to closest settlment
        distance = calculate_distance_to_closest_settlement(tile, settlement_locations)
        ExplorationProject._create_project(
            name="Exploring " + str(tile),
            needed=20 * distance,
            last_spent=civilization.last_year_updated,
            civilization=civilization,
            territory=tile,
        )

        return redirect("/" + str(civilization_id) + "/")
    # Get all the tiles around your tiles.
    neighbors = civilization.possible_exploration_tiles()

    tiles_info = []
    for tile_neighbor in neighbors:
        cost = calculate_maintance_cost_for_tile(
            tile_neighbor,
            settlement_locations=civilization.get_all_settlement_locations(),
            simple=True,
        )
        tiles_info.append(
            {
                "id": tile_neighbor.id,
                "name": str(tile_neighbor),
                "assets": tile_neighbor.assets,
                "cost": cost,
            }
        )

    context = {
        "civilization": civilization,
        "tiles": tiles_info,
    }
    return render(request, "new_exploration.html", context)


def convert_input_to_resources_spent(data):
    resources_spent = []
    for key in data:
        if "maintance_" in key:
            shorten_key = key.replace("maintance_", "")
            if "tile_" in shorten_key:
                tile_id = shorten_key.replace("tile_", "")
                tile = Tile.objects.get(id=tile_id)
                resources_spent.append(
                    {
                        "type": "maintance_tile",
                        "spent_on": tile,
                        "spent": int(data[key]),
                    }
                )
            if "tech_" in shorten_key:
                tech_id = shorten_key.replace("tech_", "")
                tech = CivTec.objects.get(id=tech_id)
                resources_spent.append(
                    {
                        "type": "maintance_tech",
                        "spent_on": tech,
                        "spent": int(data[key]),
                    }
                )
        if "project_" in key:
            project_id = key.replace("project_", "")
            project = Project.objects.get(id=project_id)
            resources_spent.append(
                {
                    "type": "project",
                    "spent_on": project,
                    "spent": int(data[key]),
                }
            )
    return resources_spent
