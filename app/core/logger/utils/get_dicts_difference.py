def get_dicts_difference(previous: dict, updated: dict):
    previous_set = set(previous.items())
    updated_set = set(updated.items())

    return updated_set - previous_set
