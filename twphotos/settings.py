import ConfigParser
import os
import sys


USER_DIR = os.path.join(os.path.expanduser('~'))
USER_CONFIG = os.path.join(USER_DIR, '.twphotos')
_d = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(_d, os.pardir))
TEST_CONFIG = os.path.join(PROJECT_PATH, '.twphotos')
TEST_DATA = os.path.join(PROJECT_PATH, 'testdata')
SECTIONS = {
    'CREDENTIALS': 'credentials',
    'INCREMENTS': 'increments',
}

# For local development
sys.path.insert(1, os.path.join(PROJECT_PATH, 'python-twitter'))

config = ConfigParser.ConfigParser()

if os.environ.get('TWPHOTOS_TEST_CONFIG'):
    CONFIG = TEST_CONFIG
else:
    CONFIG = USER_CONFIG

config.read(CONFIG)

_items = {}
CREDENTIAL_NAMES = (
    'consumer_key',
    'consumer_secret',
    'access_token_key',
    'access_token_secret',
)

if config.has_section(SECTIONS['CREDENTIALS']):
    _items = dict(config.items(SECTIONS['CREDENTIALS']))
    for name in _items:
        if name not in CREDENTIAL_NAMES:
            raise Exception('Unknown name "%s" in credentials section' % name)

if len(_items) < 4:
    raise Exception('No credentials found.')

# Credentials
CONSUMER_KEY = _items.get(CREDENTIAL_NAMES[0])
CONSUMER_SECRET = _items.get(CREDENTIAL_NAMES[1])
ACCESS_TOKEN = _items.get(CREDENTIAL_NAMES[2])
ACCESS_TOKEN_SECRET = _items.get(CREDENTIAL_NAMES[3])

# Other settings
COUNT_PER_GET = 200
MEDIA_SIZES = ('large', 'medium', 'small', 'thumb')
PROGRESS_FORMATTER = \
    'Downloading %(media_url)s from %(user)s: %(index)d/%(total)d'
NUM_THREADS = 8
TIMELINE_TYPES = ('user', 'favorites')