import json
import os
import shutil
import sys
import traceback
from enum import Enum
from pathlib import Path
import pandas as pd
import yaml
from checks import run_checks
from log import get_logger
from saturn import (saturn_get_bundle, saturn_get,auth)
from util import (PathCorrection, format_date, encrypt_pdf, save_config,
                  init_dates, init_fields)
from coa import (get_coa_filename, fill_template, get_mapping_name,
                 exec_c)
from pypdf import PdfReader

class CoatActions(Enum):
    COA = (1,)
    INIT = (2,)
    CHECK = (3,)
    FETCH = (4,)
    NONE = (5,)
    CONFIG = 6

    @staticmethod
    def map(given: str):
        return ACTION_MAP.get(given, None)


ACTION_MAP = {
    "coa": CoatActions.COA,
    "init": CoatActions.INIT,
    "check": CoatActions.CHECK,
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
        logger.info(
            "CoA creation has started, first checking and gathering data!"
        )
        if "models" not in config:
            raise KeyError("Missing 'models' section in config")
        
        user, passkey = auth(args)
        logger.info("Fetching data for the given cartridges")
        datas = saturn_get_bundle(
            args.ids, user, passkey, args.start, args.end
        )
        pdf_outputs = []
        mapping_rows = []
        mapping_set: dict[str, list] = {}
        prod_map = pd.read_excel(PathCorrection(config["prod_code_map"]).as_path())

        logger.info(
            "Data gathered sucessfully, now creating CoA"
        )
        for data in datas:
            logger.info(
                "creating CoA for following cartridge: %s",
                str(data.to_dict())
            )
            if model not in config["models"]:
                logger.error(
                    "Given model configuration is not setup. use 'init'\
                      action to setup the model"
                )
                raise ValueError(
                    "Given model configuration is not setup. use 'init'\
                      action to setup the model"
                )
            
            logger.debug("loading profile for cartridge ")
            profile_path = (
                PathCorrection(config["model_dir"]) / model / config["profile"]
            ).as_path()
            profile = yaml.safe_load(open(profile_path))
            filename = get_coa_filename(id, profile)
            dates = set(profile["dates"])
            fields = profile["fields"]
            id = data.id
            model = data.model_name()
            data_d = data.to_dict()

            # CoA Creation
            logger.info(
                "filling CoA template. template path: %s",
                profile["template"]
            )
            model_dir_path = Path(config["model_dir"]) / Path(model)
            template_path = (PathCorrection(model_dir_path) / profile["template"]).as_path()
            reader = PdfReader(template_path)
            
            # Data used to fill the values of the template file.
            fill_data = {}
            for rf in reader.get_form_text_fields():
                key = fields[rf]
                val: str
                if (key.startswith("@!")):
                    val = exec_c(key[2:])
                else:
                    val = data_d[key]
                
                if rf in dates:
                    val = format_date(val)
                fill_data[rf] = val

            res = fill_template(reader, fill_data, config["fontsize"])
            encrypted = encrypt_pdf(res, config["file_perm"])
            logger.info("Template filled and Encrypted. now outputing files")

            # Output Coa Files
            for dir in config["pdf_output_dir"]:
                dir_p = Path(dir)
                logger.info("Outputing to: %s", dir_p)
                os.makedirs(dir_p, exist_ok=True)
                dest_path = (dir_p / filename).with_suffix(".pdf").absolute()
                pdf_outputs.append(str(dest_path))
                with open(dest_path, "wb") as f:
                    encrypted.write(f)
            
            # Adding data to the mapping CSV
            logger.debug("Adding mapping data!")
            part_number = profile["PN"]
            prod_code = prod_map[prod_map["PartNumber"] == part_number][
                "ProdCode"
            ].values[0]
            lot_num = id
            if model not in mapping_set:
                mapping_set[model] = []
            mapping_set[model].append(
                {
                    "PartNumber": part_number,
                    "ProdCode": prod_code,
                    "LotNumber": lot_num,
                    "FileName": filename,
                }
            )  # TODO: make this robust

        logger.info("Coa creation done. Now creating mapping files!")
        csv_files = []
        for model, mapping_rows in mapping_set.items():
            logger.info("Creating mapping for %s model", model)
            mapping = pd.DataFrame(mapping_rows)
            mapping_f_name = get_mapping_name(args, model)
            logger.info("Running check on the data")
            run_checks(config=config, data=data, mapping=mapping)
            logger.info("outputting CSV mapping!")
            for dir in config["mapping_output_dir"]:
                mapping_d_path = Path(dir)
                logger.debug("Outputing mapping to %s", mapping_d_path)
                mapping_d_path.mkdir(parents=True, exist_ok=True)
                write_path = dir_p / mapping_f_name
                mapping.to_csv(write_path, index=False)
                csv_files.append(write_path.absolute)

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
    models = config.setdefault("models", [])
    model = args.model
    run_mode = args.run_mode
    template_path = PathCorrection(args.template).as_path()
    part_number = args.part_number
    profile = {"template": template_path.name}
    dir_path = PathCorrection(config["model_dir"]) / model
    save_path = (PathCorrection(dir_path) / "filled.pdf").as_path()
    
    # Create mapping directory if it doesn't exist
    dir_path = PathCorrection(Path(config["model_dir"]) / model).as_path()
    if os.path.exists(dir_path) and os.path.isfile(dir_path):
        logger.debug("Removing existing file at model dir path: %s", dir_path)
        os.remove(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)

        
    try:
        if model not in models:
            models.append(model)

        shutil.copy(template_path, dir_path)
        logger.info("Template copied to model directory.")
        
        logger.debug("Generating field map from PDF")
        reader = PdfReader(template_path)
        fill_data = {}
        for rf in reader.get_form_text_fields():
            fill_data[rf] = rf


        res = fill_template(reader, fill_data, config["fontsize"])
        res.write(save_path)
        profile['fields'] = init_fields()
        profile['dates'] = init_dates()
        profile["PN"] = part_number
        # profile["fields"], profile["dates"] = generate_field_map_from_pdf(
        #     config, template_file, model
        # )

        profile_path = dir_path / config["profile"]
        with open(profile_path, mode="w") as f:
            f.write(profile_comment + "\n")
            yaml.safe_dump(profile, f)

        config_path = PathCorrection(args.config).as_path()
        full_config = yaml.safe_load(open(config_path, mode="r"))
        full_config[run_mode] = config
        with open(config_path, mode="w+") as f:
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

def action_config_add(args, config):
    pdf_paths = args.pdf if args.pdf is not None else []
    csv_paths = args.csv if args.csv is not None else []
    logger.debug("Adding paths to config")
    prev_pdf = config["pdf_output_dir"]
    prev_csv = config["mapping_output_dir"]
    config["pdf_output_dir"] = list(set(pdf_paths) | set(prev_pdf))
    config["mapping_output_dir"] = list(set(csv_paths) | set(prev_csv))

def action_config_del(args, config):
    pdf_paths = args.pdf if args.pdf is not None else []
    csv_paths = args.csv if args.csv is not None else []
    logger.debug("Deleting paths from config")
    prev_pdf = config["pdf_output_dir"]
    prev_csv = config["mapping_output_dir"]
    config["pdf_output_dir"] = list(set(prev_pdf) - set(pdf_paths))
    config["mapping_output_dir"] = list(set(prev_csv) - set(csv_paths))

def action_config(args, config):
    logger.info("CONFIG action started with mode: %s", args.config_mode)
    try:
        if args.config_mode == "add":
            action_config_add(args, config)
        elif args.config_mode == "delete":
            action_config_del(args, config)
        if args.config_mode != "list":
            save_config(args, config)
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
    logger.info(
        "FETCH action started in RANGE mode: %s -> %s",
        args.start,
        args.end
    )
    try:
        user, passkey = auth(args)
        logger.info("Fetching Ids from saturn in the range.")
        ids = list(
            saturn_get(args.start, args.end,
                                            user, passkey)
        )
        logger.info("Fetched %d cartridge IDs", len(ids))
        print(1)
        print(json.dumps(ids))
    except Exception as e:
        print(0)
        logger.error("Error in FETCH (range) action: %s", str(e))
        logger.error("Traceback:\n%s", traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)
