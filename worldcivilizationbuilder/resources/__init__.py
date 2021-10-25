class ResourceBundle:
    """
    Assume
    food
    water
    and wildcard exist

    Should this just be a dictionary?
    """

    def __init__(self):
        self.food = 0.0
        self.water = 0.0
        self.leather = 0.0
        self.wildcard = 0.0

    def simmple_total(self):
        return int(self.food) + int(self.water) + int(self.leather) + int(self.wildcard)

    def __floordiv__(self, other):
        self.food = self.food // other
        self.water = self.water // other
        self.leather = self.leather // other
        self.wildcard = self.wildcard // other


# Reaource Name
# Todo

# todo where does this belong
def acceptable_resources_spent(resource_generated_bundle, resources_spent):
    # Todo shoudl I keep the generated resorces so I don't calculate it a secound time.
    available = resource_generated_bundle.simmple_total()
    used = total_resources_spent(resources_spent)

    return available >= used


def total_resources_spent(resources_spent):
    total = 0
    for r_s in resources_spent:
        total += r_s["spent"]

    return total
