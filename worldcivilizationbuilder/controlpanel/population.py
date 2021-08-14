def get_population_limit(settlement):
    return 20


def migrate_initial_population_to_new_settlement(new_settlement):
    """
    Moves up to 10 people for close settlements in the same civiliztion to this new one.
    (close): connected and under 4 tiles away
    (connected): all tiles stepped on to get here owned by this civiliztion
    """
    for other_settlement in new_settlement.civilization.settlements.exclude(
        id=new_settlement.id
    ):
        # Todo order thes settlements in some way that make sences, distance, population
        if _is_close(new_settlement, other_settlement):
            possible_moving_population = other_settlement.population // 3
            # Move people
            while possible_moving_population > 0:
                # move 1 person at a time inbetween settlements
                new_settlement.population += 1
                other_settlement.population -= 1
                possible_moving_population -= 1
                if new_settlement.population >= 10:
                    other_settlement.save()
                    new_settlement.save()
                    return
            other_settlement.save()
        new_settlement.save()


def _is_close(new_settlement, other_settlements):
    # todo figure out graph stuff to see if it is conencted
    return new_settlement.location.distance_between(other_settlements.location) <= 4
