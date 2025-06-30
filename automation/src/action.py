from util import fill_CoA, output_CoA_mapping, get_filename, get_mapping_name, Pathcr, generate_field_map_from_pdf,auth, output_CoA
from saturn import saturn_get_cartridge_data_past , saturn_get_cartridge_data_bundle, saturn_get_cartridge_data_range
from checks import run_checks
from pathlib import Path
import json, yaml, shutil, os, traceback, sys
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

profile_comment = """\
# Saturn data fields:
# id         : Unique cartridge ID
# build_date : Build date (YYYY-MM-DD)
# build_time : Time of build (HH:MM)
# exp_date   : Expiration date
# class_name : Name of classification
# class_code : Code of classification
# batch_num  : Batch number
# Possilbe actions: @!TEST, @!TIME
"""

def dispatch_action(args, config):
    action = CoatActions.map(args.action.lower())

    if action == CoatActions.COA:
        action_coa(args, config)    
    elif action == CoatActions.INIT:
        action_init(args, config)
    elif action == CoatActions.FETCH:
        if (args.fetch_mode == "range"): # TODO: CHANGE this !?
            action_fetch_range(args, config)
        else:
            action_fetch(args, config)
    elif action == CoatActions.NONE:
        pass
    elif action == CoatActions.CHECK:
        action_check(args, config)
    else:
        raise ValueError(f"Invalid Action type: {action}")
    
def action_check(args, config):
    try:
        auth(args)
        print(1)
    except Exception:
        print(0)
        traceback.print_exc(file=sys.stdout)

def action_coa(args, config):
    try: 
        if 'models' not in config:
            raise KeyError("Missing 'models' section in config")
        user, passkey = auth(args)
        datas = saturn_get_cartridge_data_bundle(args.ids, user, passkey)
        pdf_outputs = []
        mapping_rows = []
        created_models = set()
        prod_map = pd.read_excel(Pathcr(config['prod_code_map']).as_path())
        for _, data in enumerate(datas):
            id = data.id
            model = data.model_name()
            if model not in config['models']:
                raise ValueError("Given model configuration is not setup. use 'init' action to setup the model")
            profile = yaml.safe_load(open((Pathcr(config['model_dir']) / model / config['profile']).as_path()))
            filename = get_filename(id, profile)
            # CoA Creation
            temp_file = fill_CoA(config, profile, data.to_dict(), model)
            files = output_CoA(config, profile, temp_file, filename)
            pdf_outputs += files
            os.remove(temp_file) 
            
            # Adding data to the mapping CSV
            part_number = profile['PN']
            prod_code = prod_map[prod_map['PartNumber'] == part_number]['ProdCode'].values[0]
            lot_num = id
            created_models.add(model)
            mapping_rows.append({
                "PartNumber": part_number,
                "ProdCode": prod_code,
                "LotNumber": lot_num,
                "FileName": filename
            }) # TODO: make this robust! should not be creating rows of mapping like this!

        
        mapping = pd.DataFrame(mapping_rows)
        run_checks(config=config, data=data, mapping=mapping)
        csv_files = output_CoA_mapping(config, mapping, get_mapping_name(args))
        
        print(1)
        for f in pdf_outputs:
                print(f) 
        for c in csv_files:
            print(c)
    except Exception as e:
        print(0)
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)

    
def action_init(args, config):
    models = config.setdefault('models', [])
    model = args.model
    run_mode = args.rm
    template_file = Path(args.template)
    part_number = args.part_number


    dir_path = Pathcr(Path(config['model_dir']) / model).as_path()
    if os.path.exists(dir_path) and os.path.isfile(dir_path):
        os.remove(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy(template_file, dir_path)
    except Exception as e:
        pass
    
    
    
    # Fill fields with their names and print to it to a new file
    profile = {'template': template_file.name}
    profile['fields'], profile['dates'] = generate_field_map_from_pdf(config, template_file, model)
    profile['PN'] = part_number
    if model not in models:
        models.append(model)

    # Output
    config_path = Pathcr(args.config).as_path()
    profile_path = dir_path / config['profile'] 
    with open(profile_path, mode="w") as f:
        f.write(profile_comment + "\n")
        yaml.safe_dump(profile, f)
    full_config = yaml.safe_load(open(config_path, mode='r'))
    full_config[run_mode] = config
    with open(config_path, mode='w+') as f:
        yaml.safe_dump(full_config, f)

    if args.verbose:
        print(f"Configuartion for {model} finished succesfully!")
        print("\n Created Config: \n")
        print(yaml.dump(profile))


def action_fetch(args, config):
    try:
        user, passkey = auth(args)
        ids = saturn_get_cartridge_data_past(args.length, args.limit, user, passkey)
        print(1)
        print(json.dumps(list(ids)))
    except Exception:
        print(0)
        traceback.print_exc(file=sys.stdout)

def action_fetch_range(args, config):
    try:
        user, passkey = auth(args)
        ids = saturn_get_cartridge_data_range(args.start, args.end, user, passkey)
        print(1)
        print(json.dumps(list(ids)))
    except Exception:
        print(0)
        traceback.print_exc(file=sys.stdout)