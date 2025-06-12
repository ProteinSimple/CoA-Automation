import os, re
from util import Pathcr
from enum import Enum

class CoatActions(Enum):
    COA = 1,
    INIT = 2,
    CHECK = 3

    @staticmethod
    def map(given: str):
        return ACTION_MAP.get(given, CoatActions.INIT)

ACTION_MAP = {
    "coa" : CoatActions.COA,
    "init" : CoatActions.INIT,
    "check" : CoatActions.CHECK, 
}

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
            res =  models[selection - 1]
            return res
        except:
            print(" Bad request, please select a correct option from the cartridges! ")


def select_file(path, reg) -> str:
    files = os.listdir(path)
    pattern = re.compile(reg, re.IGNORECASE)
    filtered = [f for f in files if pattern.search(f)]
    
    if (len(filtered) < 1):
        raise FileNotFoundError(" no .pdf files in the mentioned directory! ")
    elif len(filtered) == 1:
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
        except:
            print(" Bad request, please select a correct option from the cartridges! ")
