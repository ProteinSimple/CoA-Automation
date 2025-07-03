from cli import get_args
from action import dispatch_action
from util import load_config
import sys, os



def setup(args):
    if args.verbose:
        return
    if not os.path.exists(args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
    sys.stdout = open(args.output, "w")

def main():
    # Arg Init
    args = get_args()
    setup(args)
    config = load_config(args)
    dispatch_action(args, config)

if __name__ == "__main__":    
    main()