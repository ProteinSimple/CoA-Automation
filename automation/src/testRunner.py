import unittest

from dotenv import load_dotenv
from tests import *
from tests.context import TestContext
from util import load_config

CONFIG_PATH = "config.yaml"
RUN_MODE = "test"

if __name__ == "__main__":
    config = load_config(CONFIG_PATH, RUN_MODE)
    TestContext.set_config(config)
    load_dotenv()
    unittest.main()
