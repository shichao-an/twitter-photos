import ConfigParser
from .settings import SECTIONS, CONFIG


config = ConfigParser.ConfigParser()
config.read(CONFIG)

if not config.has_section(SECTIONS['INCREMENTS']):
    config.add_section(SECTIONS['INCREMENTS'])
    with open(CONFIG, 'w') as f:
        config.write(f)


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
    config.read(CONFIG)
    for user, max_id in max_ids.items():
        config.set(SECTIONS['INCREMENTS'], user, str(max_id))
    with open(CONFIG, 'w') as f:
        config.write(f)


def remove_since_id(user):
    if config.has_option(SECTIONS['INCREMENTS'], user):
        config.remove_option(SECTIONS['INCREMENTS'], user)
    with open(CONFIG, 'w') as f:
        config.write(f)
