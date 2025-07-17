import logging
import os
import sys
from datetime import datetime

from action import dispatch_action
from cli import get_args
from log import get_logger
from util import load_config

logger = get_logger(__name__)


def setup(args):
    log_dir = os.path.expanduser("~/.coat/logfile")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "run.log")

    handle = logging.FileHandler(log_path)
    handle.setFormatter(logging.Formatter("[%(levelname)s] %(name)s - %(message)s"))
    root = logging.getLogger()
    root.handlers = []
    root.addHandler(handle)
    root.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if args.verbose:
        return
    if not os.path.exists(args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
    sys.stdout = open(args.output, "w")

    logger.info("==============================================")
    logger.info("Program started at %s", datetime.now().isoformat())
    logger.info("Logging initialized")
    logger.info("Setup done")


def main():
    # Arg Init
    args = get_args()
    setup(args)

    config = load_config(args.config, args.run_mode)
    logger.info("Config Loaded")
    dispatch_action(args, config)

    logger.info("Program finished at %s", datetime.now().isoformat())
    logger.info("==============================================")


if __name__ == "__main__":
    main()
