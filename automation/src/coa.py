import warnings
from datetime import datetime
from pathlib import Path
import pandas as pd
from pypdf import PdfReader, PdfWriter
from log import get_logger
from util import get_initial

warnings.filterwarnings("ignore")

logger = get_logger(__name__)


class CoaError(Exception):
    """Custom exception for PDF processing errors"""


COMMANDS = {
    "TIME": lambda: datetime.now().strftime("%m/%d/%Y"),
    "TEST": lambda: "Filled",
}


def exec_c(command: str) -> str:
    if command not in COMMANDS:
        raise CoaError(f"Unknown command: {command}")
    return COMMANDS[command]()


def get_coa_filename(id, profile, extn=".pdf"):
    template_name = Path(profile["template"]).stem
    return "_".join([str(id), template_name]) + extn


def fill_template(
    reader: PdfReader, fill_data: dict, fontsize: float = 12.0
) -> PdfWriter:
    """
    TODO
    """

    logger.info("Filling the CoA fields")
    reader_fields = reader.get_form_text_fields()
    writer = PdfWriter()
    for rf in reader_fields:
        val = fill_data[rf]
        logger.debug("Field is being filled: %s --> %s", rf, val)
        reader_fields[rf] = (val, "Helv", fontsize)
    reader.pages[0]
    writer.append(reader)
    writer.update_page_form_field_values(
        writer.pages[0], reader_fields, auto_regenerate=False
    )
    return writer


def get_mapping_name(args, model, name_prefix="coa_mapping", extn: str = ".csv") -> str:
    initials = get_initial(args.name)
    today = datetime.now().date()
    date = today.strftime("%b").lower() + str(today.day)
    return "_".join([name_prefix, model, initials, date]) + extn


def create_mapping_template(config) -> pd.DataFrame:
    columns_names = ["PartNumber", "ProdCode", "LotNumber", "FileName"]
    return pd.DataFrame(columns=columns_names)
