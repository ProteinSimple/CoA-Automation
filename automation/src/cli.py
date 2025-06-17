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
    
    parser.add_argument('action', type=str, help= 
                        """Action for the tool as mentioned below. not case sensetive
                        COA: coa and mapping creation action. uses information from args, config.yaml and files inside of 
                             inside of the model directory to
                        INIT: initilizing new cartridge type. Template pdf should be place in res/model/*model name* 
                        CHECK: NotImplemented""")
    
    parser.add_argument('--id', type=str, default=None, help="Id of the cartridge passed to the system. *REQUIRED* for action=COA")
    parser.add_argument('--list-date-length', type=int, default=5)
    parser.add_argument('--list-limit', type=int, default=50)
    parser.add_argument('--rm', type=str, default='prod',  help="Run mode")
    parser.add_argument('--model', type=str, help="Model number of cartridge")  
    parser.add_argument('--verbose', action='store_true' ,help="Print comments as process goes on")
    parser.add_argument('--config', type=str, default="config.yaml", help="YAML file containing information for running the program")
    
    return parser.parse_args()