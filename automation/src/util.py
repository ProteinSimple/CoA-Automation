import fitz, yaml, os, sys
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions
from pathlib import Path
from datetime import datetime
import pandas as pd

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

class UtilError(Exception):
    """Custom exception for PDF processing errors"""
    pass

class Pathcr:

    def __init__(self, p):
        self.path = Path(p)
    def __str__(self):
        return str(self.get_p())
    
    def __truediv__(self, p2):
        return Pathcr(self.path / str(p2))

    def get_p(self):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, str(self.path))
        return os.path.abspath(Path(__file__).parent / self.path)

    def as_path(self):
        return Path(self.get_p())

    def __repr__(self):
        return f"Pathcr({str(self)})"
    
def exec_c(command: str) -> str:
    commands = {
        "TIME": lambda: datetime.now().strftime("%d/%m/%Y"),
        "TEST": lambda: "Filled"
    }
    if command not in commands:
        raise UtilError(f"Unknown command: {command}")
    return commands[command]()

def get_filename():
    return "testOutput"    

def create_mapping(config, info, traveler_data) -> pd.DataFrame:
    """ Creates mapping using information from traveler

    Args:
        config: Configuraiton dict
        info: Information dict
        traveler_data: Traveler's Data dict
    Return val:
        Pandas DataFrame
    Exceptions:
        PDFUtilError
    """
    try:
        mapping_path: Pathcr = Pathcr(config['mapping_dir']) / info['mapping']
        mapping = pd.read_csv(mapping_path.get_p(), encoding='cp1252')
        mapping['LotNumber'] = traveler_data['lot_num']
        mapping['FileName'] = info['FileName']

        return mapping
    except Exception as e:
        raise UtilError("Failed to create CoA mapping: " + str(e))

def predict_mapping(x: str, ys: list[str]):
    """ TODO: This function is incomplete
    """

    return ""

def generate_field_map_from_pdf(config, info, model):
    
    """
        Extracts form fields from a PDF template and generates a `fields.yaml` file 
        that maps each field name to a predicted value. Additionally, creates a 
        visual preview PDF where each field is filled with its own name for reference.

    Args:
        - config (dict): Configuration dictionary containing `model_dir` and other settings.
        - info (dict): Dictionary containing metadata such as the template filename.
        - model (str): Name of the model directory where the PDF template and output files reside.

    Return val:
        - str: The filename of the generated `fields.yaml`.

    Exceptions:
        - UtilError: If the PDF cannot be opened or the YAML file cannot be generated.
        
    Notes:
        - The output PDF (`filled.pdf`) will have all form fields filled with their own names
        to help users identify field positions visually.
        - The YAML file maps each field name to a predicted target field. Placeholder predictions
        are currently used (TODO).
    """

    dir_path = Path(config['model_dir']) / Path(model)
    template_path = (Pathcr(dir_path) / info['template']).as_path()
    field_path: Path = (Pathcr(dir_path) / config['default_fields']).as_path()
    save_path = (Pathcr(dir_path) / "filled.pdf").as_path()

    try:
        doc = fitz.open(template_path)
        yaml_obj = {"fields" : {}}
        for page in doc:
            for field in page.widgets():
                field.field_value = field.field_name
                yaml_obj["fields"][field.field_name] = predict_mapping(field.field_name, [])   # TODO !!!
                field.update()
        yaml_obj['dates'] = []
        for f in yaml_obj["fields"].keys():
            if "date" in f.lower():
                yaml_obj['dates'].append(f) # TODO: This is a bad way to detect dates!
        doc.save(save_path)
        yaml.safe_dump(yaml_obj, open(field_path, mode="w+"))
        return field_path.name
    except Exception as e:        
        raise UtilError("Failed to initilize template and fields.yaml!: " + str(e))


def fill_CoA_template(config: dict, info: dict, trav_data: dict, model: str, write_path: Path | str = None) -> Path:
    """ Using the given template and fields yaml file in the directory, creates a new CoA, either in the
        specified path or in the same directory, and fills the fields given the appropriate command.
        for specs on commands see : exec_c

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

    info['fields'] = info.get('fields', config.get('default_fields'))
    # Paths used throughout the function
    dir_path = Path(config['model_dir']) / Path(model)
    template_path = (Pathcr(dir_path) / info['template']).as_path()
    field_path = (Pathcr(dir_path) / info['fields']).as_path()
    save_path = Pathcr(write_path).as_path() if write_path is not None else (Pathcr(dir_path) / "temp.pdf").as_path()
    

    try:
        doc = fitz.open(template_path)
        fields = yaml.safe_load(open(field_path))
        dates = set(fields['dates'])

        for page in doc:    
            for name, key in fields['fields'].items():
                for field in page.widgets():
                    if (field.field_name == name):
                        fn: str = field.field_name
                        val = exec_c(key[2:]) if key.startswith("@!") else trav_data[key]
                        if fn in dates: 
                            parts = val.split('/')
                            field.field_value = parts[0] + MONTH_MAP[int(parts[1])] + parts[2]
                        else:
                            field.field_value = val

                    field.update()
        
        doc.save(save_path)
        return save_path
    except Exception as e:
        raise UtilError("Failed to populating CoA: " + str(e))

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

def output_CoA_pdf(config, info, rm_input: bool = True):
    """ Outputs the filled CoA to the path specified using the two passed arguments

    Args:
        config: Config dict
        info: Information dict
    Side effects:
        removes the given input PDF file if rm_input = True
    Exceptions:
         PDFUtilError
    """
    for dir in config['pdf_output_dir']:
        dir_p = Path(dir)
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        try:
            encrypt_pdf_file(info['TempFile'], (dir_p / info['FileName']).with_suffix('.pdf'), config['file_perm'])
        except Exception as e:
            raise UtilError("Failed to output CoA PDF file: " + str(e))
    
    if rm_input: os.remove(info['TempFile']) 

def output_CoA_mapping(config, info, mapping, extn = '.csv'):
    """ Outputs the mapping data to the path specified using the two passed arguments

    Args:
        config: Config dict
        info: Information dict
    Exceptions:
         PDFUtilError
    """
    for dir in config['mapping_output_dir']:
        dir_p = Path(dir)
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        try:
            mapping.to_csv(dir_p / Path(info['FileName']).with_suffix(extn), index=False)
        except Exception as e:
            raise UtilError("Failed to output mapping excel file: " + str(e))
    
def load_config(args):
    config_path = args.config
    run_mode = args.rm
    path = Pathcr(config_path).as_path()
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    full_config = yaml.safe_load(open(path, "r"))
    if run_mode not in full_config:
        raise ValueError(f"Run mode '{run_mode}' not in config")
    return full_config[run_mode]