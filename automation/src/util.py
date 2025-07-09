import fitz, yaml, os, sys
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions
from pathlib import Path
from datetime import datetime
import pandas as pd
from typing import Self
from keyToken import load_token, add_token
from saturn import saturn_check_connection
import tempfile
from log import get_logger

logger = get_logger(__name__)
MONTH_MAP = { 1: "JAN", 2: "FEB", 3: "MAR", 4: "APR",
              5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG",
              9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC" 
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
    "TEST": lambda: "Filled"
}

class UtilError(Exception):
    """Custom exception for PDF processing errors"""
    pass

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
    
def exec_c(command: str) -> str:
    
    if command not in COMMANDS:
        raise UtilError(f"Unknown command: {command}")
    return COMMANDS[command]()

def get_filename(id, profile, extn = ".pdf"):
    
    template_name = Path(profile['template']).stem
    return "_".join([str(id), template_name]) + extn

def get_mapping_name(args, name_prefix = "coa_mapping", extn: str = ".csv") -> str:

    initials = args.name.lower()
    today = datetime.now().date()
    date = today.strftime('%b').lower() + str(today.day)
    return "_".join([name_prefix, initials, date]) + extn


def create_mapping_template(config) -> pd.DataFrame:
    columns_names = [
        'PartNumber','ProdCode',
        'LotNumber','FileName'
    ]
    return pd.DataFrame(columns=columns_names)

def predict_mapping(x: str, ys: list[str]):
    """ TODO: This function is incomplete
    """

    return ""

def generate_field_map_from_pdf(config, template, model):
    
    """
        Extracts form fields from a PDF template and generates a `fields.yaml` file 
        that maps each field name to a predicted value. Additionally, creates a 
        visual preview PDF where each field is filled with its own name for reference.

    Args:
        - config (dict): Configuration dictionary containing `model_dir` and other settings.
        - info (dict): Dictionary containing metadata such as the template filename.
        - model (str): Name of the model directory where the PDF template and output files reside.

    Return val:
        - str: The filename of the generated `fields.yaml`. TODO: Update this this is old comment

    Exceptions:
        - UtilError: If the PDF cannot be opened or the YAML file cannot be generated.
        
    Notes:
        - The output PDF (`filled.pdf`) will have all form fields filled with their own names
        to help users identify field positions visually.
        - The YAML file maps each field name to a predicted target field. Placeholder predictions
        are currently used (TODO).
    """

    dir_path = Path(config['model_dir']) / Path(model)
    template_path = Pathcr(template).as_path()
    save_path = (Pathcr(dir_path) / "filled.pdf").as_path()

    try:
        doc = fitz.open(template_path)
        retVal = {}
        for page in doc:
            for field in page.widgets():
                field.field_value = field.field_name
                retVal[field.field_name] = predict_mapping(field.field_name, [])   # TODO !!!
                field.update()
        dates = []
        for f in retVal.keys():
            if "date" in f.lower():
                dates.append(f) # TODO: This is a bad way to detect dates!
        doc.save(save_path)
        return retVal, dates
    except Exception as e:        
        raise UtilError("Failed to initilize template and fields.yaml!: " + str(e))


def fill_CoA(config: dict, info: dict, trav_data: dict, model: str, write_path: Path | str = None) -> Path:
    """ Using the given template and fields yaml file in the directory, creates a new CoA, either in the
        specified path or in the same directory, and fills the fields given the appropriate command.
        for specs on COMMANDS see : exec_c

    Args:
        - dir_path: Path to the Directory containing the fields.yaml and PDF template
        - info: Information dict
        - fill_data: Data of traveler
        - write_path: Output path
    Returns:
        - Path to the output file
    Exceptions:
        - PDFUtilError
    """

    # Paths used throughout the function
    dir_path = Path(config['model_dir']) / Path(model)
    template_path = (Pathcr(dir_path) / info['template']).as_path()
    
    if write_path is not None:
        save_path = Pathcr(write_path).as_path()
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            save_path = Path(tmp.name)
    
    doc = fitz.open(template_path)
    fields = info['fields']
    dates = set(info['dates'])
    logger.info("Filling the CoA fields. saving the result in %s", save_path)
    for page in doc:    
        for name, key in fields.items():
            for field in page.widgets():
                if (field.field_name == name):
                    logger.debug("Field is being filled: %s --> %s", name, key)
                    fn: str = field.field_name
                    val = exec_c(key[2:]) if key.startswith("@!") else trav_data[key]
                    if fn in dates: 
                        parts = val.split('/')
                        field.field_value = parts[1] + MONTH_MAP[int(parts[0])] + parts[2]
                    else:
                        logger.debug("%s was detected as date!", name)
                        field.field_value = str(val)
                field.text_fontsize =  config['fontsize']
                field.text_font = config['font']
                field.update()

    doc.save(save_path)
    return save_path

def encrypt_pdf_file(f_path: str, write_path: str, permissions: dict):
    """ Writes the given file to specified path, with the given permissions

    Args:
        - f_path: Input file
        - write_path: output path
        - permissions: permsissions dictionary
    Exceptions:
        - PDFUtilError
    """
    file_perm = 0
    for perm, flag in PERM_MAP.items():
        if (permissions.get(perm, False)):
            file_perm |= flag
    
    try:
        with open(write_path, "wb") as f:
            reader = PdfReader(f_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(
                user_password="",
                owner_password="P@$$word1!", 
                permissions_flag=file_perm
            )        
            writer.write(f)
    except Exception as e:
        raise UtilError("Failed to create CoA mapping: " + str(e))

def output_CoA(config, info, input_path, dest_filename):
    """ Outputs the filled CoA to the path specified using the two passed arguments

    Args:
        config: Config dict
        info: Information dict
    Side effects:
        removes the given input PDF file if rm_input = True
    Exceptions:
         PDFUtilError
    """ # TODO: Update this
    for dir in config['pdf_output_dir']:
        dir_p = Path(dir)
        logger.info("Outputing to: %s", dir_p)
        os.makedirs(dir_p, exist_ok=True)

        try:
            dest_path = (dir_p / dest_filename).with_suffix('.pdf')
            logger.info("Encrypting following")
            encrypt_pdf_file(input_path, dest_path, config['file_perm'])
            yield str(dest_path.absolute())
        except Exception as e:
            raise UtilError("Failed to output CoA PDF file: " + str(e))

def output_CoA_mapping(config, mapping: pd.DataFrame, mapping_f_name = "mapping.csv"):
    """ Outputs the mapping data to path specified in config

    Args:
        config: Config dict containing 'mapping_output_dir' list of directory paths
        mapping: pandas DataFrame to be saved
        mapping_f_name: Base filename (default: "mapping")
    
    Returns:
        list[str]: List of absolute file paths where mapping was saved
    """
    if 'mapping_output_dir' not in config:
        raise KeyError("'mapping_output_dir' not found in config")
    
    output_paths = []
    for dir in config['mapping_output_dir']:
        dir_path = Path(dir)
        logger.debug("Outputting mapping to %s", dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)
        write_path = (dir_path / mapping_f_name)
        try:
            mapping.to_csv(write_path, index=False)
            output_paths.append(write_path.absolute())
        except Exception as e:
            raise OSError(f"Failed to write mapping file to {write_path}: {e}")
    return output_paths
        
def load_config(args):
    """Load configuration settings from a YAML file based on specified run mode.
    
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
            f"Run mode '{run_mode}' not found. Available modes: {available_modes}"
        )
    return full_config[run_mode]


    
def auth(args):
    logger.info("trying to authenticate to saturn API")
    if hasattr(args, "user") and hasattr(args, "passkey") and args.user and args.passkey:
        logger.debug("New credentials given for saturn authentication: %s %s", args.user, args.passkey)
        add_token(args.user, args.passkey)
    else:
        logger.debug("Creadentials not given in the arguments. trying to load from cache")
    user, passkey = None, None
    try:
        logger.debug("Loading user/passkey to auth into staurn")
        user, passkey = load_token()
        assert saturn_check_connection(user, passkey)
        logger.info("Saturn auth was succesful :) !")
        return user, passkey
    except Exception as e:
        raise Exception("Couldn't load saturn API key correctly: " + str(e))