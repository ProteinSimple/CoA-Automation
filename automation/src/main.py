import yaml
from argparse import ArgumentParser
from util import fill_CoA_template, output_CoA_mapping, output_CoA_pdf, get_filename, create_mapping, Pathcr, generate_field_map_from_pdf
from terminal import model_menu, select_file, CoatActions
from checks import run_checks
from pathlib import Path

data = {
    "ref_num" : "6350527431",
    "start_date" : "27/05/2025",
    "exp_date" : "31/05/2026",
    "lot_num" : "242206PJ-A"
}

def main():
    parser = ArgumentParser(" CoA creation program ", description=" This program uses pre-made templates alongside data from travelers to create CoA pdf")
    parser.add_argument('action', type=str, help= 
                        """Action for the tool as mentioned below. not case sensetive
                        COA: coa and mapping creation action. uses information from args, config.yaml and files inside of 
                             inside of the model directory to
                        INIT: initilizing new cartridge type. Template pdf should be place in res/model/*model name* 
                        CHECK: NotImplemented""")
    parser.add_argument('--run-mode', type=str, default='prod',  help="Run mode")
    parser.add_argument('--model', type=str, help="Model number of cartridge")  
    parser.add_argument('--verbose', action='store_true' ,help="Print comments as process goes on")
    parser.add_argument('--config', type=str, default="config.yaml", help="YAML file containing information for running the program")

 
    # Arg Init
    args = parser.parse_args()
    action = CoatActions.map(args.action.lower())
    run_mode = args.run_mode
    config = yaml.safe_load(open(Pathcr(args.config).as_path(), mode='r'))[run_mode]
    model = args.model if args.model is not None else model_menu(config)

    # Take Action
    if action == CoatActions.COA:
        # Create the given CoAs using the provided data from MOPHO
        info = config['models'].get(model, None)
        if info is None:
            raise ValueError("Given model configuration is not setup. use 'init' action to setup the model")
        info['FileName'] = get_filename()
        path = fill_CoA_template(config, info, data, model)
        info['TempFile'] = path

        mapping = create_mapping(config, info, data)
        run_checks(config=config, info=info, data=data, mapping=mapping) 
        # Output the data
        output_CoA_pdf(config, info)
        output_CoA_mapping(config, info, mapping)
        print("CoA and mapping files created succesfully !")

    if action == CoatActions.INIT:
        # Get the name of template file
        dir_path = Pathcr(Path(config['model_dir']) / model).as_path()
        template_name = select_file(dir_path, r"\.pdf$")
        config['models'][model] = {}
        config['models'][model]['template'] = template_name
        # Get the name of the mapping file
        mapping_dir = Pathcr(config['mapping_dir']).as_path()
        mapping_name = select_file(mapping_dir, r"\.csv$")
        config['models'][model]['mapping'] = mapping_name
        # Fill fields with their names and print to it to a new file
        info = config['models'][model]
        fields_name = generate_field_map_from_pdf(config, info, model)
        config['models'][model]['fields'] = fields_name

        # Output
        read = yaml.safe_load(open(Pathcr(args.config).as_path(), mode='r'))
        read[run_mode] = config
        yaml.safe_dump(read, open(Pathcr(args.config).as_path(), mode='w+'))
        print(f"Configuartion for {model} finished succesfully!")
        if args.verbose:
            print("\n Created Config: \n")
            print(yaml.dump(config['models'][model]))
        
    
    if action == CoatActions.CHECK:
        raise NotImplemented("CoA Automation: CHECK action is not implemented yet!")

if __name__ == "__main__":    
    main()