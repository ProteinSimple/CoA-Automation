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

def create_mapping(config, info, trav_data) -> pd.DataFrame:
    """ Creates mapping using information from traveler

    Args:
        config: Configuraiton dict
        info: Information dict
        trav_data: Traveler's Data dict
    Return val:
        Pandas DataFrame
    Exceptions:
        PDFUtilError
    """
    try:
        mapping = pd.read_csv((Pathcr(config['mapping_dir']) / info['mapping']).get_p(), encoding='cp1252')
        mapping['LotNumber'] = trav_data['lot_num']
        mapping['FileName'] = info['FileName']

        return mapping
    except Exception as e:
        raise UtilError("Failed to create CoA mapping: " + str(e))


def populate_CoA(dir_path: Path, info: dict, trav_data: dict, write_path: Path | str = None) -> Path:
    """ Using the given template and fields yaml file in the directory, creates a new CoA, either in the
        specified path or in the same directory, and fills the fields given the appropriate command.
        for specs on commands see : exec_c

        Args:
            dir_path: Path to the Directory containing the fields.yaml and PDF template
            info: Information dict
            fill_data: Data of traveler
            write_path: Output path
        Returns:
            Path to the output file
        Exceptions:
            PDFUtilError
    """
    # Paths used throughout the function
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

def encrypte_PDF_file(f_path: str, write_path: str, permissions: dict):
    """ Writes the given file to specified path, with the given permissions

    Args:
        f_path: Input file
        write_path: output path
        permissions: permsissions dictionary
    Exceptions:
        PDFUtilError
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
        dir_p = Pathcr(dir).as_path()
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        try:
            encrypte_PDF_file(info['TempFile'], (dir_p / info['FileName']).with_suffix('.pdf'), config['file_perm'])
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
    
