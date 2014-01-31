import ConfigParser
import os
import sys


USER_DIR = os.path.join(os.path.expanduser('~'))
USER_CONFIG = os.path.join(USER_DIR, '.twphotos')
d = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(os.path.join(d, os.pardir))
TEST_CONFIG = os.path.join(PROJECT_PATH, '.twphotos')
# For local development
sys.path.insert(1, os.path.join(PROJECT_PATH, 'python-twitter'))

config = ConfigParser.ConfigParser()
if os.environ.get('TWPHOTOS_TEST_CONFIG'):
    config.read(TEST_CONFIG)
else:
    config.read(USER_CONFIG)

items = {}
item_names = [
    'consumer_key',
    'consumer_secret',
    'access_token_key',
    'access_token_secret',
]

if config.has_section('credentials'):
    items = dict(config.items('credentials'))
    for name in items:
        if name not in item_names:
            raise Exception('Unknown name "%s" in credentials section' % name)

if len(items) < 4:
    raise Exception('No credentials found.')

CONSUMER_KEY = items.get('consumer_key')
CONSUMER_SECRET = items.get('consumer_secret')
ACCESS_TOKEN = items.get('access_token_key')
ACCESS_TOKEN_SECRET = items.get('access_token_secret')


COUNT_PER_GET = 200
MEDIA_SIZES = ['large', 'medium', 'small', 'thumb']
PROGRESS_FORMATTER = \
    'Downloading %(media_url)s from %(user)s: %(index)d/%(total)d'
NUM_THREADS = 8
