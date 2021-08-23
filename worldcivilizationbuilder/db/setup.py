from db.disaster import Disaster
from db.technology import Technology


def create_base_data():
    create_base_disaster_data()
    create_base_technology_data()


def create_base_disaster_data():
    if Disaster.DISEASE_OUTBREAK is None:
        Disaster.create(name="Disease Outbreak")
    if Disaster.DRAUGHT is None:
        Disaster.create(name="Draught")
    if Disaster.FOREST_FIRE is None:
        Disaster.create(name="Forest Fire")
    if Disaster.IN_FIGHTING is None:
        Disaster.create(name="In Fighting")
    if Disaster.UNTIMELY_DEATH is None:
        Disaster.create(name="Untimely Death")


def create_base_technology_data():
    if Technology.get(name=Technology.BONE_TOOLS_NAME) is None:
        Technology.create(
            name=Technology.BONE_TOOLS_NAME,
            tech_type="Technology",
            # Todo Is there a better way to format this...?
            description="""
Can make Bone Harpoons and Bone Spears
+1 on martial fights if used as weapons
Can Hunt
Can Spear Fish
1/4 more reeasourese from rivers.
            """,
            prerequisite=None,
            needed_maintance=1,
        )

    if Technology.get(name=Technology.FIRE_NAME) is None:
        Technology.create(
            name=Technology.FIRE_NAME,
            tech_type="Technology",
            description="Acess to Fire.",
        )

    if Technology.get(name=Technology.BOILING_WATER_NAME) is None:
        Technology.create(
            name=Technology.BOILING_WATER_NAME,
            tech_type="Technology",
            # Todo Is there a better way to format this...?
            description="""
You can claim land next to the ocean as thou they are rivers.
            """,
            prerequisite=Technology.get(name=Technology.FIRE_NAME).id,
        )

    if Technology.get(name=Technology.COMPOSITE_TOOLS_NAME) is None:
        Technology.create(
            name=Technology.COMPOSITE_TOOLS_NAME,
            tech_type="Technology",
            # Todo Is there a better way to format this...?
            description="""
Can make Flint Spears, Flint Axes, Flint Picks
+2 on martial fights if used as weapons
Can gather flint from hills
Can chop wood in the forests
Can not hunt if cutting wood.
            """,
            prerequisite=Technology.get(name=Technology.BONE_TOOLS_NAME).id,
            # todo find a way to forces the maintance type.
            needed_maintance=2,
        )
        # Todo maybe add a Technology for knowing what flint is.

    if Technology.get(name=Technology.TANNING_NAME) is None:
        Technology.create(
            name=Technology.TANNING_NAME,
            tech_type="Technology",
            description="Gain 1 extra reasource when hunting around a town.",
        )

    if Technology.get(name=Technology.FOOD_DRYING_NAME) is None:
        Technology.create(
            name=Technology.FOOD_DRYING_NAME, tech_type="Technology", description="TODO"
        )

    if Technology.get(name=Technology.DOMESTICATED_DOGS_NAME) is None:
        Technology.create(
            name=Technology.DOMESTICATED_DOGS_NAME,
            tech_type="Technology",
            description="1/4 more from hunting",
        )

    if Technology.get(name=Technology.SOAP_NAME) is None:
        Technology.create(
            name=Technology.SOAP_NAME,
            tech_type="Technology",
            description="Effects from Disease are reduced by 1/4",
        )

    if Technology.get(name=Technology.SLINGS_NAME) is None:
        Technology.create(
            name=Technology.SLINGS_NAME,
            tech_type="Technology",
            description="""
Can make Slings
+2 on martial fights if used as weapons
Can hunt
            """,
            needed_maintance=1,
        )
