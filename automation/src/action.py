import json
import os
import shutil
import sys
import traceback
from enum import Enum
from pathlib import Path
import pandas as pd
import yaml
from pypdf import PdfReader
from checks import run_checks
from coa import exec_c, fill_template, get_coa_filename, get_mapping_name
from log import get_logger
from saturn import (auth, saturn_bundle_data, saturn_bundle_prod_data,
                    find_analysis_range, CartridgeData)
from util import (PathCorrection, encrypt_pdf, format_date, init_dates,
                  init_fields, init_fonts, save_config)
import io


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
}

profile_comment = \
"""
# Saturn data fields:
# id         : Unique cartridge ID
# build_date : Build date (YYYY-MM-DD)
# build_time : Time of build (HH:MM)
# exp_date   : Expiration date
# class_name : Name of classification
# class_code : Code of classification
# batch_num  : Batch number
# passed_qc  : Cartridge QC results
# qc_date    : Date of QC (YYYY-MM-DD)
# qc_time    : Time of QC (HH:MM)
# qc_status  : PASS or a FAIL
# qc_user    : QC Analyst name
# Possilbe actions: @!TEST, @!TIME
"""

logger = get_logger(__name__)
global buffer
buffer = None


def print_b(s: str):
    buffer.write(str(s) + "\n")


def dispatch_action(args, config):
    action = CoatActions.map(args.action.lower())
    logger.info("Action %s initiated", action)
    global buffer
    buffer = io.StringIO()
    try:
        if action == CoatActions.COA:
            action_coa(args, config)
        elif action == CoatActions.INIT:
            action_init(args, config)
        elif action == CoatActions.FETCH:
            action_fetch(args, config)
        elif action == CoatActions.CONFIG:
            action_config(args, config)
        elif action == CoatActions.CHECK:
            action_check(args, config)
        else:
            raise ValueError(f"Invalid Action type: {action}")

        print(1)
        print(buffer.getvalue())
        logger.info(1)
    except Exception as e:
        print(0)
        logger.error("Error in actions: %s", str(e))
        logger.error(traceback.format_exc())
        sys.stdout.flush()
        traceback.print_exc(file=sys.stdout)


def action_check(args, config):
    logger.info("Running CHECK action")
    auth(args)


def action_coa(args, config):
    logger.info("CoA creation has started, checking and gathering data!")
    if "models" not in config:
        raise KeyError("Missing 'models' section in config")

    user, passkey = auth(args)
    logger.info("Fetching data for the given cartridges")
    res = saturn_bundle_prod_data(user, passkey, args.start, args.end)
    datas = list(filter(lambda v: v.id in set(args.ids), res))
    pdf_outputs = []
    mapping_rows = []
    mapping_set: dict[str, list] = {}
    prod_map = pd.read_excel(
        PathCorrection(config["prod_code_map"]).as_path()
    )
    logger.info("Data gathered sucessfully, now creating CoA")
    for data in datas:
        logger.info(
            "creating CoA for following cartridge: %s",
            str(data.to_dict())
        )
        if data.model_name() not in config["models"]:
            logger.error(
                "Given model configuration is not setup. use 'init'\
                    action to setup the model"
            )
            raise ValueError(
                "Given model configuration is not setup. use 'init'\
                    action to setup the model"
            )

        logger.debug("loading profile for cartridge ")
        model = data.model_name()
        data_d = data.to_dict()
        id = data.id
        profile_path = (
            PathCorrection(config["model_dir"]) / model / config["profile"]
        ).as_path()
        profile: dict
        with open(profile_path) as f:
            profile = yaml.safe_load(f)
        filename = get_coa_filename(id, profile)
        dates = set(profile["dates"])
        fields = profile["fields"]
        fonts = profile.get("font", dict())

        # CoA Creation
        logger.info("filling CoA template. template path: %s", profile["template"])
        model_dir_path = Path(config["model_dir"]) / Path(model)
        template_path = (
            PathCorrection(model_dir_path) / profile["template"]
        ).as_path()
        reader = PdfReader(template_path)

        # Data used to fill the values of the template file.
        fill_data = {}
        font_data = {}
        default_font = config["fontsize"]
        for rf in reader.get_form_text_fields():
            key = fields[rf]
            val: str
            if key.startswith("@!"):
                val = exec_c(key[2:])
            else:
                val = data_d[key]

            if rf in dates:
                val = format_date(val)
            fill_data[rf] = val
            font_data[rf] = \
                fonts[rf] if (rf in fonts and fonts[rf] is not None and fonts[rf] != "") \
                else default_font
        logger.debug(font_data)
        res = fill_template(reader, fill_data, font_data)
        encrypted = encrypt_pdf(res, config["file_perm"])
        logger.info("Template filled and Encrypted. now outputing files")

        # Output Coa Files
        for dir in config["pdf_output_dir"]:
            pdf_dir_path = Path(dir)
            logger.info("Outputing to: %s", pdf_dir_path)
            os.makedirs(pdf_dir_path, exist_ok=True)
            dest_path = (pdf_dir_path / filename).with_suffix(".pdf").absolute()
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
            write_path = mapping_d_path / mapping_f_name
            mapping.to_csv(write_path, index=False)
            csv_files.append(write_path.absolute())

    logger.info("COA creation finshed succesfully!")
    for f in pdf_outputs:
        print_b(f)
    for c in csv_files:
        print_b(c)


def action_init(args, config):
    logger.info("INIT action started for model: %s", args.model)
    models = config.setdefault("models", [])
    # Values used for filling the profile
    model = args.model
    code = args.code
    run_mode = args.run_mode
    color = args.color
    part_number = args.part_number
    default_fontsize = config['fontsize']
    # Paths used throughout the function
    template_path = PathCorrection(args.template).as_path()
    dir_path = PathCorrection(Path(config["model_dir"]) / model).as_path()
    save_path = dir_path / "filled.pdf"
    map_path = PathCorrection(config['code_map']).as_path()
    profile_path = dir_path / config["profile"]
    config_path = PathCorrection(args.config).as_path()
    # We will fill this as we go along
    profile = {"template": template_path.name}
    # Create mapping directory if it doesn't exist
    if os.path.exists(dir_path) and os.path.isfile(dir_path):
        logger.debug("Removing existing file at model dir path: %s", dir_path)
        os.remove(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    if model not in models:
        models.append(model)

    CartridgeData.add_code2map(map_path, code, model)
    shutil.copy(template_path, dir_path)
    logger.info("Template copied to model directory.")
    logger.debug("Generating field map from PDF")
    reader = PdfReader(template_path)
    fill_data = {}
    font_data = {}
    for rf in reader.get_form_text_fields():
        fill_data[str(rf)] = str(rf)  # Put the name of the field as the value of the field
        font_data[str(rf)] = default_fontsize
    res = fill_template(reader, fill_data, font_data)
    res.write(save_path)
    profile["fields"] = init_fields(fill_data)
    profile["dates"] = init_dates(fill_data)
    profile["font"] = init_fonts(fill_data, config["fontsize"])
    profile["PN"] = part_number
    profile["color"] = color

    with open(profile_path, mode="w") as f:
        f.write(profile_comment + "\n")
        yaml.safe_dump(profile, f)
    # Update the config file with the new cartridge data
    full_config = yaml.safe_load(open(config_path, mode="r"))
    full_config[run_mode] = config
    with open(config_path, mode="w+") as f:
        yaml.safe_dump(full_config, f)

    logger.info("INIT completed successfully for model: %s", model)


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
    mode = args.config_mode
    logger.info("CONFIG action started with mode: %s", mode)
    if mode == "add":
        action_config_add(args, config)
    elif mode == "delete":
        action_config_del(args, config)
    if mode != "list":
        save_config(args.config, args.run_mode, config)
        logger.info("CONFIG updated successfully")
    print_b(json.dumps(config))


def action_fetch(args, config):
    logger.info("FETCH action started in RANGE mode: %s -> %s", args.start, args.end)
    user, passkey = auth(args)
    logger.info("Fetching Ids from saturn in the range.")
    res = saturn_bundle_data(user, passkey, args.start, args.end)
    analysis_start, analysis_end = find_analysis_range(res)
    res = [v.to_dict() for v in res]
    color_map = {}
    for v in res:
        code = v["class_code"]
        if (code not in CartridgeData.code_map):
            continue  # Old cartridge !
        model = CartridgeData.code_map[code]
        if code not in color_map:
            profile_path = (
                PathCorrection(config["model_dir"]) / model / config["profile"]
            ).as_path()
            with open(profile_path) as f:
                profile = yaml.safe_load(f)
                color_map[code] = profile["color"]
        v["color"] = color_map[code]
    retVal = {
        "values": res,
        "prod_start": saturn_bundle_data.prod_start,
        "prod_end": saturn_bundle_data.prod_end,
        "analysis_start": analysis_start,
        "analysis_end": analysis_end
    }
    logger.info("Fetched %d cartridge IDs", len(res))
    print_b(json.dumps(retVal))
