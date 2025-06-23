from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser(
        " CoA creation program ",
        description= " This program uses pre-made templates alongside data from travelers to create CoA pdf"
    )

    subparsers = parser.add_subparsers(dest='action', required=True, help='Action to perform')
    sub_list: list[ArgumentParser] = []
    sub_list.append(coa_sub := subparsers.add_parser('coa', help='Coa and mapping creation action. uses information from args, config.yaml and files inside of inside of the model directory to'))
    sub_list.append(coa_bun_sub := subparsers.add_parser('coa_bun', help=' Coa bundle action '))
    sub_list.append(init_sub := subparsers.add_parser('init', help='Initilizing new cartridge type. Template pdf should be place in res/model/*model name*'))
    sub_list.append(fetch_sub := subparsers.add_parser('fetch', help='Fetches'))
    sub_list.append(none_sub := subparsers.add_parser('none', help='Does nothing; mostly for debugging purpose'))
    sub_list.append(check_sub := subparsers.add_parser('check', help='checks the connection to all the end points including the following (Updated as more endpoints added) : [Saturn, Mopho]'))
    
    # specific argument passed to certain actions:
    coa_sub.add_argument('id', type=str, help="Id of the cartridge passed to the system")
    
    fetch_sub.add_argument('length', type=int) # TODO: add help to these two
    fetch_sub.add_argument('limit', type=int)
    

    init_sub.add_argument('model', type=str, help="Model number of cartridge")
    init_sub.add_argument('template', type=str)
    init_sub.add_argument('mapping', type=str)

    for sub in sub_list:
        sub.add_argument('--rm', type=str, default='test',  help="Run mode")
        sub.add_argument('--verbose', action='store_true' ,help="Print comments as process goes on")
        sub.add_argument('--config', type=str, default="config.yaml", help="YAML file containing information for running the program")
        sub.add_argument('--output', type=str, default=r'./log1.txt', help="output path for the program")
        sub.add_argument('--user', type=str, required=False)
        sub.add_argument('--passkey', type=str, required=False) # TODO : add comments for these

    

    return parser.parse_args()