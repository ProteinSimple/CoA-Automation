from util import fill_CoA_template, output_CoA_mapping, output_CoA_pdf, get_filename, create_mapping, Pathcr, generate_field_map_from_pdf,auth
from util import create_mapping_template, output_CoA_pdf_v2
from saturn import saturn_get_cartridge_data_range , saturn_get_cartridge_data, saturn_get_cartridge_data_bundle
from checks import run_checks
from pathlib import Path
import json, yaml, shutil, os
from enum import Enum
import pandas as pd

class CoatActions(Enum):
    COA = 1,
    INIT = 2,
    CHECK = 3,
    FETCH = 4,
    COA_BUNDLE= 5,
    NONE = 6

    @staticmethod
    def map(given: str):
        return ACTION_MAP.get(given, None)

ACTION_MAP = {
    "coa" : CoatActions.COA,
    "init" : CoatActions.INIT,
    "check" : CoatActions.CHECK,
    "fetch": CoatActions.FETCH,
    "none": CoatActions.NONE, 
}

data = {
    "ref_num" : "6350527431",
    "start_date" : "27/05/2025",
    "exp_date" : "31/05/2026",
    "lot_num" : "242206PJ-A"
}

def dispatch_action(args, config):
    action = CoatActions.map(args.action.lower())

    if action == CoatActions.COA:
        action_coa(args, config)    
    elif action == CoatActions.INIT:
        action_init(args, config)
    elif action == CoatActions.FETCH:
        action_list_id(args, config)
    elif action == CoatActions.NONE:
        pass
    elif action == CoatActions.CHECK:
        action_check(args, config)
    else:
        raise ValueError(f"Invalid Action type: {action}")
    
def action_check(args, config):
    try:
        auth(args, config)
        print(1)
    except BaseException:
        print(0)

def action_coa(args, config):
    if 'models' not in config:
        raise KeyError("Missing 'models' section in config")
    
    user, passkey = auth(args, config)
    datas = saturn_get_cartridge_data_bundle(args.ids, user, passkey)
    pdf_outputs = []
    mapping_rows = []
    prod_map = pd.read_excel(Pathcr(config['prod_code_map']).get_p())

    try: 
        for _, data in enumerate(datas):
            id = data.id
            model = data.model_name()
            if config['models'].get(model, None) is None:
                raise ValueError("Given model configuration is not setup. use 'init' action to setup the model")
            info = config['models'][model]
            filename = get_filename(id)
            
            # CoA Creation
            temp_file = fill_CoA_template(config, info, data.to_dict(), model)
            files = output_CoA_pdf_v2(config, info, temp_file, filename)
            pdf_outputs += files
            os.remove(temp_file) 
            
            # Adding data to the mapping CSV
            part_number = info['PN']
            prod_code = prod_map[prod_map['PartNumber'] == part_number]['ProdCode'].values[0]
            lot_num = id
            file_name = get_filename(id)
            
            mapping_rows.append({
                "PartNumber": part_number,
                "ProdCode": prod_code,
                "LotNumber": lot_num,
                "FileName": file_name
            }) # TODO: make this robust! should not be creating rows of mapping like this!
        
        mapping = pd.DataFrame(mapping_rows)
        run_checks(config=config, info=info, data=data, mapping=mapping)
        csv_files = output_CoA_mapping(config, info, mapping)
        
        print(1)
        for f in pdf_outputs:
                print(f) 
        for c in csv_files:
            print(c)
    except Exception as e:
        print(0)
        raise BaseException("Failed to create given CoAs " + str(e))

        



    
def action_init(args, config):
    models = config.setdefault('models', {})
    model = args.model
    run_mode = args.rm
    template_file = Path(args.template)
    mapping_file = Path(args.mapping)



    dir_path = Pathcr(Path(config['model_dir']) / model).as_path()
    try:
        shutil.copy(template_file, dir_path)
        shutil.copy(mapping_file, dir_path)
    except Exception as e:
        pass
    
    model_config = {
        'template': template_file.name,
        'mapping': mapping_file.name,
    }
    
    # Fill fields with their names and print to it to a new file
    model_config['fields'] = generate_field_map_from_pdf(config, model_config, model)
    models[model] = model_config

    
    # Output
    config_path = Pathcr(args.config).as_path()
    full_config = yaml.safe_load(open(config_path, mode='r'))
    full_config[run_mode] = config
    yaml.safe_dump(full_config, open(config_path, mode='w+'))

    if args.verbose:
        print(f"Configuartion for {model} finished succesfully!")
        print("\n Created Config: \n")
        print(yaml.dump(config['models'][model]))


def action_list_id(args, config):
    try:
        user, passkey = auth(args, config)
        ids = saturn_get_cartridge_data_range(args.length, args.limit, user, passkey)
        print(json.dumps(list(ids)))
    except Exception:
        pass

