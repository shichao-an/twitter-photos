from .settings import config, SECTIONS, CONFIG


if not config.has_section(SECTIONS['INCREMENTS']):
    config.add_section(SECTIONS['INCREMENTS'])


def read_since_ids(users):
    """
    Read max ids of the last downloads

    :param users: A list of users

    Return a dictionary mapping users to ids
    """
    since_ids = {}
    for user in users:
        if config.has_option(SECTIONS['INCREMENTS'], user):
            since_ids[user] = config.getint(SECTIONS['INCREMENTS'], user) + 1
    return since_ids


def set_max_ids(max_ids):
    """
    Set max ids of the current downloads

    :param max_ids: A dictionary mapping users to ids
    """
    for user, max_id in max_ids.items():
        config.set(SECTIONS['INCREMENTS'], user, max_id)
    with open(CONFIG, 'w') as f:
        config.write(f)
