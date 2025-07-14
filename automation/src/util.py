import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Self

import pandas as pd
import yaml
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions

from log import get_logger
logger = get_logger(__name__)
MONTH_MAP = {
    1: "JAN",
    2: "FEB",
    3: "MAR",
    4: "APR",
    5: "MAY",
    6: "JUN",
    7: "JUL",
    8: "AUG",
    9: "SEP",
    10: "OCT",
    11: "NOV",
    12: "DEC",
}


PERM_MAP = {
    "print": UserAccessPermissions.PRINT,
    "modify": UserAccessPermissions.MODIFY,
    "copy": UserAccessPermissions.EXTRACT,
    "form_fill": UserAccessPermissions.FILL_FORM_FIELDS,
    "annotate": UserAccessPermissions.ADD_OR_MODIFY,
    "accessibility": UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS,
    "assemble": UserAccessPermissions.ASSEMBLE_DOC,
    "extract": UserAccessPermissions.EXTRACT,
}

COMMANDS = {
    "TIME": lambda: datetime.now().strftime("%m/%d/%Y"),
    "TEST": lambda: "Filled",
}


class UtilError(Exception):
    """Custom exception for PDF processing errors"""


class Pathcr:
    def __init__(self, p):
        self.path = Path(p)

    def __str__(self):
        return str(self._get_p())

    def __truediv__(self, p2) -> Self:
        return Pathcr(self.path / str(p2))

    def _get_p(self):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, str(self.path))
        return os.path.abspath(Path(__file__).parent / self.path)

    def as_path(self) -> Path:
        return Path(self._get_p())

    def __repr__(self):
        return f"Pathcr({str(self)})"


def get_initial(args):
    name: str = args.name.lower()
    return "".join([s[0].lower() for s in name.split(" ")])

def predict_mapping(x: str, ys: list[str]):
    """TODO: This function is incomplete"""

    return ""

def format_date(given: str):
    parts = given.split("/") 
    return parts[1] + MONTH_MAP[int(parts[0])] + parts[2]

def encrypt_pdf(writer: PdfWriter, permissions: dict) -> PdfWriter:
    """Writes the given file to specified path, with the given permissions

    Args:
        - f_path: Input file
        - write_path: output path
        - permissions: permsissions dictionary
    Exceptions:
        - PDFUtilError
    """
    file_perm = 0
    for perm, flag in PERM_MAP.items():
        if permissions.get(perm, False):
            file_perm |= flag

    writer.encrypt(
        user_password="",
        owner_password="P@$$word1!",
        permissions_flag=file_perm,
    )
    return writer


def load_config(args):
    """Load configuration settings from a YAML file based on specified run
       mode.

    Args:
        args: Parsed command line arguments with config and rm attributes

    Returns:
        dict: Configuration dictionary for the specified run mode

    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        ValueError: If the specified run mode is not found in the config
        yaml.YAMLError: If the YAML file is malformed
    """

    config_path = args.config
    run_mode = args.rm
    path = Pathcr(config_path).as_path()
    full_config = None

    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            full_config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Failed to parse YAML file: {e}")

    if run_mode not in full_config:
        available_modes = list(full_config.keys())
        raise ValueError(
            f"""Run mode '{run_mode}' not found.
              Available modes: {available_modes}"""
        )
    return full_config[run_mode]

