import os
os.environ['TWPHOTOS_TEST_CONFIG'] = '0'
import shutil
from unittest import TestCase
from .settings import PROJECT_PATH
from .photos import TwitterPhotos


TEST_OUTPUT = 'test-output'
TEST_USER = 'WIRED'


class TestPhotos(TestCase):
    """Test TwitterPhotos class programmatically"""
    def setUp(self):
        d = os.path.join(PROJECT_PATH, TEST_OUTPUT)
        if not os.path.exists(d):
            os.makedirs(d)
        self.directory = d

    def test_credentials(self):
        pass

    def test_get(self):
        twphotos = TwitterPhotos(TEST_USER)
        p = twphotos.get(count=20)

    def test_download(self):
        twphotos = TwitterPhotos(user=TEST_USER, outdir=self.directory)
        p = twphotos.get(count=20)
        twphotos.download()
        self.assertEqual(len(p), len(os.listdir(self.directory)))

    def tearDown(self):
        shutil.rmtree(self.directory)
