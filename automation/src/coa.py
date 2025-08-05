import warnings
from datetime import datetime
from pathlib import Path
import pandas as pd
from pypdf import PdfReader, PdfWriter
from log import get_logger
from util import get_initial
import fitz 
from io import BytesIO

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
    reader: PdfReader, fill_data: dict, fontsize: float = 12.0, font: str = "helv"
) -> PdfWriter:
    """
    TODO
    """

    logger.info("Filling the CoA fields")
    original_stream = BytesIO()
    reader.pages[0]
    writer = PdfWriter()
    writer.append(reader)
    writer.write(original_stream)
    original_stream.seek(0)
    
    doc = fitz.open(stream=original_stream.read(), filetype="pdf")
    for page in doc:
        for widget in page.widgets():
            if widget.field_name in fill_data:
                widget.field_value = str(fill_data[widget.field_name])
                widget.text_fontsize =  fontsize
                widget.text_font = font
                widget.update()
    updated_pdf_bytes = doc.write()
    doc.close()
    updated_stream = BytesIO(updated_pdf_bytes)
    updated_reader = PdfReader(updated_stream)
    final_writer = PdfWriter()
    updated_reader.pages[0]
    final_writer.append(updated_reader)
    return final_writer


def get_mapping_name(args, model, name_prefix="coa_mapping", extn: str = ".csv") -> str:
    initials = get_initial(args.name)
    today = datetime.now().date()
    date = today.strftime("%b").lower() + str(today.day)
    return "_".join([name_prefix, model, initials, date]) + extn


def create_mapping_template(config) -> pd.DataFrame:
    columns_names = ["PartNumber", "ProdCode", "LotNumber", "FileName"]
    return pd.DataFrame(columns=columns_names)
