import json
import re

import pandas as pd

from log import get_logger
from util import Pathcr

"""
    The following file contains the checks that are done after the
    mapping and the pdf files are created.
    All of the functions are responsible for the following:
        1- checking if their arguments are avaiable in the provided
           kwargs
        2- importing their own arguments
        3- returning boolean as a return value

    To add a new check to the pipeline follow these steps:
    1 - if your function requires data outside of the ones provided
        by the function "run_checks" make sure to alter the function
        to pass the data correctly

    2 - Write your function using the following formula:

        def function_name(**kwargs) -> bool:
            * Make sure to explain what are checking for with comments
            * Check and Import arguments *
            ...
            if (check true):
                return True
            return False
    3 - Add your function to the list of functions (assertions)
        in the bottom of the list

"""
logger = get_logger(__name__)


class CheckError(Exception):
    pass


def run_checks(**kwargs):
    """Helper function from main"""
    for f in ASSERTIONS:
        if not f(**kwargs):
            logger.error(
                " The following check failed to pass: " +
                f.__name__
            )
            raise CheckError(
                " The following check failed to pass: " +
                f.__name__
            )
    return True


def check_columns(**kwargs) -> bool:
    """
    Checks if the name mapping file columns are similar to the
    ones listed on the appropriate json file
    Requires:
        - config object
        - mapping pandas DF
    """
    if "config" not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'config'")
    if "mapping" not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'mapping'")

    config: dict = kwargs["config"]
    mapping: pd.DataFrame = kwargs["mapping"]

    with open(Pathcr(config["mapping_columns"]).as_path()) as f:
        if json.load(f) != sorted(mapping.columns.values):
            return False

    return True


def check_prodcode_matching(**kwargs):
    """
    Checks if the PartNumber listed on the mapping corresponds to ones
    listed in the Western/Biologics excel map
    Requires:
        - config object
        - mapping pandas DF
    """
    if "config" not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'config'")
    if "mapping" not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'mapping'")

    config: dict = kwargs["config"]
    mapping: pd.DataFrame = kwargs["mapping"]
    prod_path = Pathcr(config["prod_code_map"]).as_path()
    prod_code = pd.read_excel(prod_path)
    expected = prod_code[
        prod_code["PartNumber"] == mapping["PartNumber"].values[0]
    ]["ProdCode"]
    actual = mapping["ProdCode"]
    if expected.values[0].strip() != actual.values[0].strip():
        return False
    if not re.match(r"^[a-zA-Z0-9\-|]+$", actual.values[0]):
        return False

    return True


"""
    List of all of the checks that the program will import and use.
    Add the name of the function associated with your check
    to the following list.
"""
ASSERTIONS = [check_columns, check_prodcode_matching]
