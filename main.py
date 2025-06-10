import yaml
from argparse import ArgumentParser
from util import populate_CoA, output_CoA_mapping, output_CoA_pdf, get_filename, create_mapping
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
            return False, f
    return True, None

def main():
    parser = ArgumentParser(" CoA creation program ", description=" This program uses pre-made templates alongside data from travelers to create CoA pdf")
    parser.add_argument('--run-mode', type=str, default='prod')
    parser.add_argument('--model', type=str, required=True) 
    parser.add_argument('--verbose', action='store_true')

    args = parser.parse_args()
    dirc = args.model
    run_mode = args.run_mode
    config = yaml.safe_load(open(f"config.yaml", mode='r'))[run_mode]
    info = config['models'][dirc]
    info['FileName'] = get_filename()

    # Create the given CoAs using the provided data from MOPHO
    path = populate_CoA(Path(config['model_dir']) / Path(dirc), info, data)
    info['TempFile'] = path
    mapping = create_mapping(config, info, data)
    res, f = run_checks(config=config, info=info, data=data, mapping=mapping) 
    if res == False:
        print("Unsuccesful checks: the following check failed :", f.__name__) 
        return
    
    # Output the data
    output_CoA_pdf(config, info)
    output_CoA_mapping(config, info, mapping)

if __name__ == "__main__":    
    main()