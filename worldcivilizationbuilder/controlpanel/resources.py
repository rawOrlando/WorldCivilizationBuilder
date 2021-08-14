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
