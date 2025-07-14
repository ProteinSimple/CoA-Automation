from pypdf import PdfReader, PdfWriter
import pandas as pd
from datetime import datetime
from pathlib import Path
from util import Pathcr, get_initial, predict_mapping
from log import get_logger
import fitz

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



@DeprecationWarning
def generate_field_map_from_pdf(config, template, model):
    """
        Extracts form fields from a PDF template and generates a `fields.yaml`
        file that maps each field name to a predicted value. Additionally,
        creates a visual preview PDF where each field is filled with its own
        name for reference.

    Args:
        - config (dict): Configuration dictionary containing `model_dir` and
                         other settings.
        - info (dict): Dictionary containing metadata such as the template
                       filename.
        - model (str): Name of the model directory where the PDF template and
                       output files reside.

    Return val:
        - str: The filename of the generated `fields.yaml`.
               TODO: Update this this is old comment

    Exceptions:
        - UtilError: If the PDF cannot be opened or the YAML file cannot be
                     generated.

    Notes:
        - The output PDF (`filled.pdf`) will have all form fields filled with
          their own names to help users identify field positions visually.
        - The YAML file maps each field name to a predicted target field.
          Placeholder predictions
        are currently used (TODO).
    """

    dir_path = Path(config["model_dir"]) / Path(model)
    template_path = Pathcr(template).as_path()
    save_path = (Pathcr(dir_path) / "filled.pdf").as_path()

    try:
        doc = fitz.open(template_path)
        retVal = {}
        for page in doc:
            for field in page.widgets():
                field.field_value = field.field_name
                retVal[field.field_name] = predict_mapping(
                    field.field_name, []
                )  # TODO !!!
                field.update()
        dates = []
        for f in retVal.keys():
            if "date" in f.lower():
                dates.append(f)  # TODO: This is a bad way to detect dates!
        doc.save(save_path)
        return retVal, dates
    except Exception as e:
        raise CoaError(
            "Failed to initilize template and fields.yaml!: " +
            str(e)
        )



def fill_template(reader: PdfReader, fill_data: dict, fontsize: float = 12.0) -> PdfWriter :
    """
        TODO
    """
    
    logger.info("Filling the CoA fields")
    reader_fields = reader.get_form_text_fields()
    writer = PdfWriter()
    for rf in reader_fields:
        val = fill_data[rf]
        logger.debug("Field is being filled: %s --> %s", rf, val)
        reader_fields[rf] = (val , "", fontsize)
    page = reader.pages[0]
    writer.append(reader)
    writer.update_page_form_field_values(
        writer.pages[0],
        reader_fields,
        auto_regenerate=False
    )
    return writer


def get_mapping_name(args, model, name_prefix="coa_mapping",
                     extn: str = ".csv") -> str:
    initials = get_initial(args)
    today = datetime.now().date()
    date = today.strftime("%b").lower() + str(today.day)
    return "_".join([name_prefix, model, initials, date]) + extn


def create_mapping_template(config) -> pd.DataFrame:
    columns_names = ["PartNumber", "ProdCode", "LotNumber", "FileName"]
    return pd.DataFrame(columns=columns_names)
