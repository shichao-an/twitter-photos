#!/usr/bin/env python
import os
from twphotos.photos import main


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
config = os.path.join(PROJECT_PATH, '.twphotos')
os.environ['TWPHOTOS_TEST_CONFIG'] = config
main()
