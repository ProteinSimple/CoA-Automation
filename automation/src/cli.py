import os, re
from util import Pathcr
from argparse import ArgumentParser

ENV_FILE = '.env'



def init_env(path):
    print("Enviroment file not found!")
    api_user = input("Enter API username: ").strip()
    api_pass = input("Enter API password: ").strip()
    content = f"API_USER={api_user}\nAPI_PASS={api_pass}\n"
    with open(path, "w") as f:
        f.write(content)

def model_menu(config) -> str:
    model_dir = Pathcr(config['model_dir']).as_path()
    models = os.listdir(model_dir)

    count = 0
    mult = 0
    col_count = 4
    print("\n" * 2)
    for model in models:
        count += 1
        print(f"  [{count + mult * col_count}] {model}  ", end="")
        if (count == col_count): 
            count = 0
            mult += 1
            print("\n") # new line
    
    print("\n" * 2)
    while True:
        try:
            selection = int(input("Please select the model of the cartridge:    ").strip())
            print(selection)
            res =  models[selection - 1]
            return res
        except Exception:
            print(" Bad request, please select a correct option from the cartridges! ")
        except KeyboardInterrupt:
            print(" Keyboard interrup detected, exiting with code 1!")
            exit(1)


def select_file(path, reg, verbose=False) -> str:
    files = os.listdir(path)
    pattern = re.compile(reg, re.IGNORECASE)
    filtered = [f for f in files if pattern.search(f)]
    
    if (len(filtered) < 1):
        raise FileNotFoundError(" no .pdf files in the mentioned directory! ")
    elif len(filtered) == 1:
        if verbose:
            print("only one option; writing to :" + filtered[0])
        return filtered[0]
    
    count = 0
    mult = 0
    col_count = 4
    print("\n" * 2)
    for f in filtered:
        count += 1
        print(f"  [{count + mult * col_count}] {f}  ", end="")
        if (count == col_count): 
            count = 0
            mult += 1
            print("\n") # new line
        
    
    print("\n" * 2)
    while True:
        try:
            selection = int(input("Please select the model of the cartridge:    ").strip())
            res =  filtered[selection - 1]
            return res
        except Exception:
            print(" Bad request, please select a correct option from the cartridges! ")
        except KeyboardInterrupt:
            print(" Keyboard interrup detected, exiting with code 1!")
            exit(1)


def get_args():
    parser = ArgumentParser(
        " CoA creation program ",
        description= " This program uses pre-made templates alongside data from travelers to create CoA pdf"
    )

    subparsers = parser.add_subparsers(dest='action', required=True, help='Action to perform')
    sub_list: list[ArgumentParser] = []
    sub_list.append(coa_sub := subparsers.add_parser('coa', help='coa and mapping creation action. uses information from args, config.yaml and files inside of inside of the model directory to'))
    sub_list.append(init_sub := subparsers.add_parser('init', help='initilizing new cartridge type. Template pdf should be place in res/model/*model name*'))
    sub_list.append(fetch_sub := subparsers.add_parser('fetch', help='f'))
    sub_list.append(none_sub := subparsers.add_parser('none', help='Does nothing; mostly for debugging purpose'))
    sub_list.append(check_sub := subparsers.add_parser('check', help='NOT IMPLEMENTED'))
    
    # specific argument passed to certain actions:
    coa_sub.add_argument('id', type=str, help="Id of the cartridge passed to the system")
    coa_sub.add_argument('--model', type=str, help="Model number of cartridge")  
    
    fetch_sub.add_argument('length', type=int) # TODO: add help to these two
    fetch_sub.add_argument('limit', type=int)

    init_sub.add_argument('--model', type=str, help="Model number of cartridge")

    for sub in sub_list:
        sub.add_argument('--rm', type=str, default='prod',  help="Run mode")
        sub.add_argument('--verbose', action='store_true' ,help="Print comments as process goes on")
        sub.add_argument('--config', type=str, default="config.yaml", help="YAML file containing information for running the program")
        sub.add_argument('--output', type=str, default='.out', help="output path for the program")
    

    return parser.parse_args()