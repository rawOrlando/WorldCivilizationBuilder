from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse

from db.civilization import Civilization, Settlement
from db.map import Tile
from controlpanel.models import CivTec
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
    from db.setup import create_base_data

    create_base_data()
    civilization_list = Civilization.all()
    context = {
        "civilization_list": civilization_list,
    }
    return render(request, "civilization_list.html", context)


def civilization(request, civilization_id):
    civilization = Civilization.get(_id=civilization_id)
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


## Todo these 3 views pages to make a new civilization
def new_civilization(request):
    if request.POST:
        civ = Civilization.create(name=request.POST["name"])

        tile1_id = request.POST["tile1"].replace("tile_", "")
        tile2_id = request.POST["tile2"].replace("tile_", "")
        tile3_id = request.POST["tile3"].replace("tile_", "")

        tile1 = Tile.get(_id=tile1_id)
        tile1.controler_id = civ.id
        tile1.save()

        print(tile2_id)
        tile2 = Tile.get(_id=tile2_id)
        print(tile2)
        print(tile1)
        tile2.controler_id = civ.id
        tile2.save()

        tile3 = Tile.get(_id=tile3_id)
        tile3.controler_id = civ.id
        tile3.save()

        spot = request.POST["spot"]
        if spot == 1:
            location_id = tile1_id
        elif spot == 2:
            location_id = tile2_id
        else:
            location_id = tile3_id

        Settlement.create(
            name=request.POST["cap_name"],
            civilization_id=civ.id,
            location_id=location_id,
            population=15,
            is_capital=True,
        )

        # todo cahnge this to use redirect
        return redirect("/")

    from tinydb import Query

    tiles = Tile.filter(Query().controler_id is None)
    tiles = Tile.all()
    print(tiles)
    context = {
        "tiles": tiles_to_info(tiles),
    }
    return render(request, "new_civilization.html", context)


def new_civilization_land(request, civilization_id):
    from tinydb import Query

    tiles = Tile.filter(Query().controler_id is None)
    print(tiles)
    context = {
        "tiles": tiles_to_info(tiles),
    }

    return render(request, "new_civilization.html", context)


def new_civilization_capital(request):
    pass


def new_tile(request):
    from map.assets import ALL_ASSETS

    if request.POST:
        # Get the Assets from post request
        assets = list(set(ALL_ASSETS).intersection(set(request.POST.keys())))

        Tile.create(
            x=request.POST["x"],
            y=request.POST["y"],
            z=request.POST["z"],
            resources=assets,
        )

    context = {
        "assets": ALL_ASSETS,
    }
    return render(request, "new_tile.html", context)


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

    context = {
        "civilization": civilization,
        "tiles": tiles_to_info(tiles),
    }
    return render(request, "new_settlement.html", context)


def tiles_to_info(tiles):
    tiles_info = []
    for tile in tiles:
        tiles_info.append(
            {
                "id": tile.id,
                "name": str(tile),
                "assets": tile.resources,
            }
        )
    return tiles_info


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
