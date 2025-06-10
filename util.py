from pdfrw import PdfReader, PdfWriter
import fitz, yaml
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions
from pathlib import Path
from datetime import datetime
import pandas as pd

month_map = { 1: "JAN", 2: "FEB", 3: "MAR", 4: "APR",
              5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG",
              9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC" 
            }

perm_map = {
    "print": UserAccessPermissions.PRINT,
    "modify": UserAccessPermissions.MODIFY,     
    "copy": UserAccessPermissions.EXTRACT,
    "form_fill": UserAccessPermissions.FILL_FORM_FIELDS,     
    "annotate": UserAccessPermissions.ADD_OR_MODIFY,
    "accessibility": UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS,        
    "assemble": UserAccessPermissions.ASSEMBLE_DOC,         
    "extract": UserAccessPermissions.EXTRACT,
}

def exec_c(com: str) -> str:
    match com:
        case "TIME":
            return datetime.now().strftime("%d/%m/%Y")
        case "TEST":
            return "Filled"

def get_filename():
    return "testOutput"    

def create_mapping(config, info, trav_data) -> pd.DataFrame:
    mapping = pd.read_csv(Path(config['mapping_dir']) / Path(info['mapping']), encoding='cp1252')
    mapping['LotNumber'] = trav_data['lot_num']
    mapping['FileName'] = info['FileName']

    return mapping


def fill_fields(dir_path: Path, info, fill_data):
    template_path = dir_path / Path(info['template'])
    field_path = dir_path / Path("fields.yaml")
    save_path = dir_path / Path("filled.pdf")

    doc = fitz.open(template_path)
    fields = yaml.safe_load(open(field_path))
    dates = set(fields['dates'])
    
    page = next(iter(doc))
    for name, key in fields['fields'].items():
        for field in page.widgets():
            if (field.field_name == name):
                fn: str = field.field_name
                val = exec_c(key[2:]) if key.startswith("@!") else fill_data[key]
                if fn in dates: 
                    parts = val.split('/')
                    field.field_value = parts[0] + month_map[int(parts[1])] + parts[2]
                else:
                    field.field_value = val

            field.update()
    
    doc.save(save_path)
    return save_path

def encrypte_file(f_path: str, write_path: str, permissions: dict):
    reader = PdfReader(f_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    
    file_perm = 0
    for perm, flag in perm_map.items():
        if (permissions.get(perm, False)):
            file_perm |= flag


    writer.encrypt(
        user_password="",
        owner_password="admin123", 
        permissions_flag=file_perm
    )
    with open(write_path, "wb") as f:
        writer.write(f)


