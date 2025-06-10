import os, yaml, sys
from argparse import ArgumentParser
from util import fill_fields, encrypte_file, get_filename, create_mapping
from checks import assertions
from pathlib import Path


data = {
    "ref_num" : "6350527431",
    "start_date" : "27/05/2025",
    "exp_date" : "31/05/2026",
    "lot_num" : "242206PJ-A"
}



def run_checks(**kwargs):
    for f in assertions:
        if not f(**kwargs):
            return False
    return True

def main():
    parser = ArgumentParser(" CoA creation program ", description=" This program uses pre-made templates alongside data from travelers to create CoA pdf")
    parser.add_argument('--run-mode', type=str, default='prod')
    parser.add_argument('--model', type=str, required=True) 
    parser.add_argument('--verbose', action='store_true')

    args = parser.parse_args()
    dirc = args.model
    rm = args.run_mode
    config = yaml.safe_load(open(f"config.yaml", mode='r'))[rm]
    

    # Create the given CoAs using the provided data from MOPHO
    info = config['models'][dirc]
    path = fill_fields(Path(config['model_dir']) / Path(dirc), info, data)
    info['FileName'] = get_filename()
    

    mapping = create_mapping(config, info, data)
    if not run_checks(config=config, info=info, data=data, mapping=mapping):
        print(" Unsuccesful checks") 
        exit(1)
        return
    
    # Output the data
    for dir in config['pdf_output_dir']:
        dir_p = Path(dir)
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        try:
            encrypte_file(path, dir_p / Path(info['FileName']).with_suffix('.pdf'), config['file_perm'])
        except PermissionError as p:
            print("While trying to write to listed path the follwing error occured", file=sys.stderr)
            print(f"Path: {dir}", file=sys.stderr)
            print(str(p), file=sys.stderr)
    
    for dir in config['mapping_output_dir']:
        dir_p = Path(dir)
        if (not os.path.exists(dir_p)):
            os.makedirs(dir_p)
        try:
            mapping.to_csv(dir_p / Path(info['FileName']).with_suffix('.csv'), index=False)
        except Exception as e:
            print("While trying to write to listed path the follwing error occured", file=sys.stderr)
            print(f"Path: {dir}", file=sys.stderr)
            print(str(p), file=sys.stderr)
    
    os.remove(path)

    

main()