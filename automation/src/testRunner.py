import unittest
from tests import *
from dotenv import load_dotenv
from tests.context import TestContext
from util import load_config, PathCorrection
from saturn import CartridgeData
import logging
CONFIG_PATH = "config.yaml"
RUN_MODE = "test"

if __name__ == "__main__":
    root = logging.getLogger()
    logging.disable(logging.WARNING)
    logging.disable(logging.CRITICAL)
    config = load_config(CONFIG_PATH, RUN_MODE)
    map_path = PathCorrection(config["code_map"]).as_path()
    CartridgeData.load_code_map(map_path)
    TestContext.set_config(config)
    load_dotenv()
    unittest.main()
