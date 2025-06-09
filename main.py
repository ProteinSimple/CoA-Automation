import os, yaml
from argparse import ArgumentParser
from util import fill_fields, encrypte_file, get_filename, create_mapping
from pathlib import Path
import json
import pandas as pd
import re


data = {
    "ref_num" : "6350527431",
    "start_date" : "27/05/2025",
    "exp_date" : "31/05/2026",
    "lot_num" : "242206PJ-A"
}


    # # 2: check that ProdCode is correct and has valid characters
    # expected = prod_code[prod_code['PartNumber'] == mapping['PartNumber'].values[0]]['ProdCode']
    # actual = mapping['ProdCode']
    # if (expected.values[0].strip() != actual.values[0].strip()):
    #     return None
    # if not re.match(r'^[a-zA-Z0-9\-|]+$', actual.values[0]):
    #     return None

    # return mapping

def check_columns(**kwargs) -> bool:
    if 'config' not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'config'")
    if 'mapping' not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'mapping'")
    
    config: dict = kwargs['config']
    mapping: pd.DataFrame = kwargs['mapping']

    with open(config['def_mapping_columns']) as f:
        if (json.load(f) != sorted(mapping.columns.values)):
            return False
    
    return True


def check_prodcode_matching(**kwargs):
    if 'config' not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'config'")
    if 'mapping' not in kwargs:
        raise KeyError(" Function didn't get the required argument: 'mapping'")
    
    config: dict = kwargs['config']
    mapping: pd.DataFrame = kwargs['mapping']


    prod_code = pd.read_excel(config['prod_code'])
    expected = prod_code[prod_code['PartNumber'] == mapping['PartNumber'].values[0]]['ProdCode']
    actual = mapping['ProdCode']
    if (expected.values[0].strip() != actual.values[0].strip()):
        return None
    if not re.match(r'^[a-zA-Z0-9\-|]+$', actual.values[0]):
        return None



assertions = [
    check_columns,
    check_prodcode_matching
]

def run_checks(config, info, data, mapping):
    
    for f in assertions:
        if not f(config=config, info=info, data=data, mapping=mapping):
            return False

def main():
    parser = ArgumentParser(" CoA creation program ", description=" This program uses pre-made templates alongside data from travelers to create CoA pdf")
    parser.add_argument('--run-mode', type=str, default='prod')
    parser.add_argument('--model', type=str, required=True) 
    parser.add_argument('--verbose', action='store_true')

    args = parser.parse_args()
    config = None
    dirc = args.model
    rm = args.run_mode
    with open(f"config.yaml", mode='r') as f:
        config = yaml.safe_load(f)[rm]
    
    # Create the given CoAs using the provided data from MOPHO
    info = config['models'][dirc]
    path = fill_fields(Path(config['model_dir']) / Path(dirc), info, data)
    info['FileName'] = get_filename()
    

    mapping = create_mapping(config, info, data)

    # Output the data
    for dir in config['pdf_output_dir']:
        dir_p = Path(dir)
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        # mapping.to_csv(dir_p / Path(info['FileName']))
        encrypte_file(path, dir_p / Path(info['FileName']).with_suffix('.csv'))
    
    for dir in config['pdf_output_dir']:
        dir_p = Path(dir)
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        mapping.to_csv(dir_p / Path(info['FileName']).with_suffix('.csv'), index=False)
    
    os.remove(path)

    

main()