from util import fill_CoA, output_CoA_mapping, get_filename, get_mapping_name, Pathcr, generate_field_map_from_pdf,auth, output_CoA
from saturn import saturn_get_cartridge_data_past , saturn_get_cartridge_data_bundle, saturn_get_cartridge_data_range
from checks import run_checks
from pathlib import Path
import json, yaml, shutil, os, traceback, sys
from enum import Enum
import pandas as pd
from log import get_logger
class CoatActions(Enum):
    COA = 1,
    INIT = 2,
    CHECK = 3,
    FETCH = 4,
    NONE = 5,
    CONFIG = 6

    @staticmethod
    def map(given: str):
        return ACTION_MAP.get(given, None)

ACTION_MAP = {
    "coa" : CoatActions.COA,
    "init" : CoatActions.INIT,
    "check" : CoatActions.CHECK,
    "fetch": CoatActions.FETCH,
    "config": CoatActions.CONFIG,
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

logger = get_logger(__name__)

def dispatch_action(args, config):
    action = CoatActions.map(args.action.lower())
    logger.info(" Action %s initiated", action)
    if action == CoatActions.COA:
        action_coa(args, config)    
    elif action == CoatActions.INIT:
        action_init(args, config)
    elif action == CoatActions.FETCH:
        action_fetch(args, config)
    elif action == CoatActions.CONFIG:
        action_config(args, config)
    elif action == CoatActions.NONE:
        pass
    elif action == CoatActions.CHECK:
        action_check(args, config)
    else:
        raise ValueError(f"Invalid Action type: {action}")
    
def action_check(args, config):
    try:
        logger.info("Running CHECK action")
        auth(args)
        print(1)
    except Exception as e:
        print(0)
        logger.error("Error in CHECK action: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)

def action_coa(args, config):
    try: 
        logger.info("CoA creation has started, first checking and gathering data!")
        if 'models' not in config:
            raise KeyError("Missing 'models' section in config")
        user, passkey = auth(args)
        logger.debug("User: %s, passkey: %s", user, passkey)
        logger.info("Fetching data for the given cartridges")
        datas = saturn_get_cartridge_data_bundle(args.ids, user, passkey)
        pdf_outputs = []
        mapping_rows = []
        created_models = set()
        prod_map = pd.read_excel(Pathcr(config['prod_code_map']).as_path())
        logger.info("Data gathered sucessfully, now creating CoA")

        for _, data in enumerate(datas):
            logger.info("creating CoA for following cartridge: %s", str(data.to_dict()))
            id = data.id
            model = data.model_name()
            if model not in config['models']:
                logger.error("Given model configuration is not setup. use 'init' action to setup the model")
                raise ValueError("Given model configuration is not setup. use 'init' action to setup the model")
            logger.debug("loading profile for cartridge ")
            profile = yaml.safe_load(open((Pathcr(config['model_dir']) / model / config['profile']).as_path()))
            filename = get_filename(id, profile)
            # CoA Creation
            logger.info("filling CoA template. template path: %s", profile['template'])
            temp_file = fill_CoA(config, profile, data.to_dict(), model)
            logger.info("Template filled. now outputing files")
            files = output_CoA(config, profile, temp_file, filename)
            pdf_outputs += files
            os.remove(temp_file) 
            
            # Adding data to the mapping CSV
            logger.debug("Adding mapping data!")
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

        logger.info("Creating mapping file")
        mapping = pd.DataFrame(mapping_rows)
        run_checks(config=config, data=data, mapping=mapping)
        csv_files = output_CoA_mapping(config, mapping, get_mapping_name(args))
        logger.info("COA creation finshed succesfully! ")
        print(1)
        for f in pdf_outputs:
                print(f) 
        for c in csv_files:
            print(c)
    except Exception as e:
        print(0)
        logger.error("Exception occurred: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)

    
def action_init(args, config):
    logger.info("INIT action started for model: %s", args.model)
    models = config.setdefault('models', [])
    model = args.model
    run_mode = args.rm
    template_file = Path(args.template)
    part_number = args.part_number

    dir_path = Pathcr(Path(config['model_dir']) / model).as_path()
    if os.path.exists(dir_path) and os.path.isfile(dir_path):
        logger.debug("Removing existing file at model dir path: %s", dir_path)
        os.remove(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy(template_file, dir_path)
        logger.info("Template copied to model directory.")
    except Exception as e:
        logger.warning("Failed to copy template: %s", str(e))

    try:
        logger.debug("Generating field map from PDF")
        profile = {'template': template_file.name}
        profile['fields'], profile['dates'] = generate_field_map_from_pdf(config, template_file, model)
        profile['PN'] = part_number
        if model not in models:
            models.append(model)

        profile_path = dir_path / config['profile']
        with open(profile_path, mode="w") as f:
            f.write(profile_comment + "\n")
            yaml.safe_dump(profile, f)

        config_path = Pathcr(args.config).as_path()
        full_config = yaml.safe_load(open(config_path, mode='r'))
        full_config[run_mode] = config
        with open(config_path, mode='w+') as f:
            yaml.safe_dump(full_config, f)

        logger.info("INIT completed successfully for model: %s", model)

        if args.verbose:
            print(f"Configuration for {model} finished successfully!")
            print("\n Created Config: \n")
            print(yaml.dump(profile))

    except Exception as e:
        print(0)
        logger.error("Error during INIT: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)

def action_config(args, config):
    logger.info("CONFIG action started with mode: %s", args.config_mode)
    try:
        pdf_paths = args.pdf if args.pdf is not None else []
        csv_paths = args.csv if args.csv is not None else []

        if args.config_mode == "add":
            logger.debug("Adding paths to config")
            prev_pdf = config['pdf_output_dir']
            prev_csv = config['mapping_output_dir']
            config['pdf_output_dir'] = list(set(pdf_paths) | set(prev_pdf))
            config['mapping_output_dir'] = list(set(csv_paths) | set(prev_csv))

        elif args.config_mode == "delete":
            logger.debug("Deleting paths from config")
            prev_pdf = config['pdf_output_dir']
            prev_csv = config['mapping_output_dir']
            config['pdf_output_dir'] = list(set(prev_pdf) - set(pdf_paths))
            config['mapping_output_dir'] = list(set(prev_csv) - set(csv_paths))

        config_path = args.config
        p = Pathcr(config_path).as_path()
        logger.debug("Writing config file to %s", p)

        if args.config_mode != "list":
            full_config = yaml.safe_load(open(p, mode='r'))
            full_config[args.rm] = config
            with open(p, mode="w+") as f:
                yaml.safe_dump(full_config, f)

        logger.info("CONFIG updated successfully")
        print(1)
        json.dump(config, sys.stdout)

    except Exception as e:
        print(0)
        logger.error("Error in CONFIG action: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)




def action_fetch(args, config):
    logger.info("FETCH action started in mode: %s", args.fetch_mode)
    if args.fetch_mode == "range":
        return action_fetch_range(args, config)

    try:
        user, passkey = auth(args)
        logger.info("Fetching Ids with the following limit/length: %d/%d", args.length, args.limit)
        ids = saturn_get_cartridge_data_past(args.length, args.limit, user, passkey)
        logger.info("Fetched %d cartridge IDs", len(ids))
        print(1)
        print(json.dumps(list(ids)))
    except Exception as e:
        print(0)
        logger.error("Error in FETCH (past) action: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)

def action_fetch_range(args, config):
    logger.info("FETCH action started in RANGE mode: %s -> %s", args.start, args.end)
    try:
        user, passkey = auth(args)
        logger.info("Fetching Ids from saturn in the range.")
        ids = saturn_get_cartridge_data_range(args.start, args.end, user, passkey)
        logger.info("Fetched %d cartridge IDs", len(ids))
        print(1)
        print(json.dumps(list(ids)))
    except Exception as e:
        print(0)
        logger.error("Error in FETCH (range) action: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)