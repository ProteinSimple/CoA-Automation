from cli import get_args
from action import dispatch_action
from util import load_config

def main():
    
    # Arg Init
    args = get_args()
    config = load_config(args.config, args.rm)
    dispatch_action(args, config)

if __name__ == "__main__":    
    main()