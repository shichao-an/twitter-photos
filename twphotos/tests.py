import os
os.environ['TWPHOTOS_TEST_CONFIG'] = '0'
import shutil
from unittest import TestCase
from .settings import PROJECT_PATH
from .photos import TwitterPhotos
from .utils import create_directory
from .increment import remove_since_id

TEST_OUTPUT = 'test-output'
TEST_USER = 'WIRED'
TEST_LIST_SLUG = 'ces-2014'


class TestPhotos(TestCase):
    """Test TwitterPhotos class programmatically"""
    def setUp(self):
        d = os.path.join(PROJECT_PATH, TEST_OUTPUT)
        create_directory(d)
        self.directory = d
        remove_since_id(TEST_USER)

    def test_credentials(self):
        twphotos = TwitterPhotos(test=True)
        twphotos.verify_credentials()

    def test_download(self):
        twphotos = TwitterPhotos(user=TEST_USER, outdir=self.directory,
                                 test=True)
        p = twphotos.get(count=20)
        twphotos.download()
        self.assertEqual(len(p), len(os.listdir(self.directory)))

    def test_increment_download(self):
        t1 = TwitterPhotos(user=TEST_USER, outdir=self.directory,
                           num=20, increment=True, test=True)
        photos1 = t1.get()[TEST_USER]
        self.assertEqual(len(photos1), 20)
        t1.download()
        t2 = TwitterPhotos(user=TEST_USER, outdir=self.directory,
                           num=20, increment=True, test=True)
        photos2 = t2.get()[TEST_USER]
        self.assertEqual(len(photos2), 0)
        t2.download()

    def _test_list_download(self):
        """
        Recover this test when fixed issue #138 of python-twitter
        is released
        """
        twphotos = TwitterPhotos(user=TEST_USER, list_slug=TEST_LIST_SLUG,
                                 outdir=self.directory)
        p = twphotos.get(count=20)
        twphotos.download()
        self.assertEqual(len(p), len(os.listdir(self.directory)))

    def tearDown(self):
        shutil.rmtree(self.directory)
        remove_since_id(TEST_USER)
