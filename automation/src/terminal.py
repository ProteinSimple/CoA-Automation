import os
from util import Pathcr

def model_menu(config) -> str:
    model_dir = Pathcr(config['model_dir']).as_path()
    models = os.listdir(model_dir)

    count = 0
    mult = 0
    col_count = 4
    for model in models:
        count += 1
        print(f"  [{count + mult * col_count}] {model}  ", end="")
        if (count == col_count): 
            count = 0
            mult += 1
            print() # new line
    
    print()
    while True:
        try:
            selection = int(input("Please select the model of the cartridge:    ").strip())
            res =  models[selection - 1]
            return res
        except:
            print(" Bad request, please select a correct option from the cartridges! ")
