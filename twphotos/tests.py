import os
os.environ['TWPHOTOS_TEST_CONFIG'] = '0'
import shutil
from unittest import TestCase
from .settings import PROJECT_PATH
from .photos import TwitterPhotos
from .utils import create_directory


TEST_OUTPUT = 'test-output'
TEST_USER = 'WIRED'
TEST_LIST_SLUG = 'ces-2014'


class TestPhotos(TestCase):
    """Test TwitterPhotos class programmatically"""
    def setUp(self):
        d = os.path.join(PROJECT_PATH, TEST_OUTPUT)
        create_directory(d)
        self.directory = d

    def test_credentials(self):
        twphotos = TwitterPhotos()
        twphotos.verify_credentials()

    def test_get(self):
        twphotos = TwitterPhotos(TEST_USER)
        p = twphotos.get(count=20)

    def test_download(self):
        twphotos = TwitterPhotos(user=TEST_USER, outdir=self.directory)
        p = twphotos.get(count=20)
        twphotos.download()
        self.assertEqual(len(p), len(os.listdir(self.directory)))

    def test_list_download(self):
        twphotos = TwitterPhotos(user=TEST_USER, list_slug=TEST_LIST_SLUG,
                                 outdir=self.directory)
        p = twphotos.get(count=20)
        twphotos.download()
        self.assertEqual(len(p), len(os.listdir(self.directory)))
        
    def tearDown(self):
        shutil.rmtree(self.directory)
