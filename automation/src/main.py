from cli import get_args
from action import dispatch_action
from util import load_config
import sys
def setup(args):
    sys.stdout = open(args.output, "w")

def terminate(args):
    sys.stdout.close()

def main():
    
    # Arg Init
    args = get_args()
    setup(args)
    config = load_config(args)
    dispatch_action(args, config)
    terminate(args)

if __name__ == "__main__":    
    main()