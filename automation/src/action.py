from util import fill_CoA_template, output_CoA_mapping, output_CoA_pdf, get_filename, create_mapping, Pathcr, generate_field_map_from_pdf
from cli import model_menu, select_file, ENV_FILE, init_env
from saturn import saturn_get_cartridge_data, saturn_check_connection
from checks import run_checks
from pathlib import Path
import json, yaml
from enum import Enum
from dotenv import load_dotenv

class CoatActions(Enum):
    COA = 1,
    INIT = 2,
    CHECK = 3,
    FETCH = 4,
    NONE = 5

    @staticmethod
    def map(given: str):
        return ACTION_MAP.get(given, None)

ACTION_MAP = {
    "coa" : CoatActions.COA,
    "init" : CoatActions.INIT,
    "check" : CoatActions.CHECK,
    "fetch": CoatActions.FETCH,
    "fetch": CoatActions.FETCH,
    "none": CoatActions.NONE  
}

data = {
    "ref_num" : "6350527431",
    "start_date" : "27/05/2025",
    "exp_date" : "31/05/2026",
    "lot_num" : "242206PJ-A"
}





def dispatch_action(args, config):
    
    env_path = Pathcr(ENV_FILE).as_path()
    action = CoatActions.map(args.action.lower())
    
    if not env_path.exists():
        while True:
            init_env(env_path)
            
            load_dotenv(env_path) 
            if (saturn_check_connection()):
                break   
            print("Bad Env Variables!")
        

    load_dotenv(env_path)
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
        raise NotImplemented("CoA Automation: CHECK action is not implemented yet!")
    else:
        raise ValueError(f"Invalid Action type: {action}")
    
def action_coa(args, config):
    if 'models' not in config:
        raise KeyError("Missing 'models' section in config")
    
    model = args.model or  model_menu(config)
    info = config['models'].get(model, None)
    if info is None:
        raise ValueError("Given model configuration is not setup. use 'init' action to setup the model")
    
    if args.id is None:
        raise ValueError("To create CoA and Mapping, ID of the cartridge is needed!")
    id = args.id
    
    info['FileName'] = get_filename()
    path = fill_CoA_template(config, info, data, model)
    info['TempFile'] = path

    mapping = create_mapping(config, info, data)
    run_checks(config=config, info=info, data=data, mapping=mapping) 
    # Output the data
    output_CoA_pdf(config, info)
    output_CoA_mapping(config, info, mapping)
    
    if args.verbose:
        print("CoA and mapping files created succesfully !")


def action_init(args, config):
    run_mode = args.rm
    models = config.setdefault('models', {})
    model = args.model or  model_menu(config)

    dir_path = Pathcr(Path(config['model_dir']) / model).as_path()
    template_name = select_file(dir_path, r"\.pdf$", args.verbose)
    
    # Get the name of the mapping file
    mapping_dir = Pathcr(config['mapping_dir']).as_path()
    mapping_name = select_file(mapping_dir, r"\.csv$", args.verbose)
    
    model_config = {
        'template': template_name,
        'mapping': mapping_name,
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
    ids = saturn_get_cartridge_data(args.length, args.limit)
    print(json.dumps(list(ids)))

