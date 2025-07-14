from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(
        " CoA creation program ",
        description=" This program uses pre-made templates alongside data\
                      data from travelers to create CoA pdf",
    )

    subparsers = parser.add_subparsers(
        dest="action", required=True, help="Action to perform"
    )
    sub_list: list[ArgumentParser] = []
    sub_list.append(
        coa_sub := subparsers.add_parser(
            "coa",
            help="Coa and mapping creation action. uses information from args,\
                  config file and templates from model profile and given ids\
                  to generate CoAs!",
        )
    )
    sub_list.append(
        init_sub := subparsers.add_parser(
            "init",
            help="Initilizing new cartridge type. Template pdf should \
                  be place in res/model/*model name*",
        )
    )
    sub_list.append(fetch_sub := subparsers.add_parser(
        "fetch",
        help="Fetches")
    )
    sub_list.append(
        _ := subparsers.add_parser(
            "none", help="Does nothing; mostly for debugging purpose"
        )
    )
    sub_list.append(
        _ := subparsers.add_parser(
            "check",
            help="checks the connection to end points",
        )
    )
    sub_list.append(config_sub := subparsers.add_parser("config", help="TODO"))

    # specific argument passed to certain actions:
    coa_sub.add_argument(
        "ids", type=int, nargs="+",
        help="Id of the cartridge for file generation"
    )
    coa_sub.add_argument("--name", type=str, default="AA")
    coa_sub.add_argument("--start", type=str, default=None)
    coa_sub.add_argument("--end", type=str, default=None)

    # Case 1: Default fetch with length and limit
    fetch_subparsers = fetch_sub.add_subparsers(
        dest="fetch_mode",
        required=False
    )
    sub_list.append(
        default_fetch := fetch_subparsers.add_parser(
            "default", help="Default fetch mode using length and limit"
        )
    )
    default_fetch.add_argument(
        "length",
        type=int,
        help="Number of items to fetch"
    )
    default_fetch.add_argument("limit", type=int, help="Limit per request")

    # Case 2: fetch range with start and end
    sub_list.append(
        range_fetch := fetch_subparsers.add_parser(
            "range", help="Fetch with a start and end range"
        )
    )
    range_fetch.add_argument("start", type=str, help="Start of the range")
    range_fetch.add_argument("end", type=str, help="End of the range")

    init_sub.add_argument("model", type=str, help="Model number of cartridge")
    init_sub.add_argument("template", type=str)
    init_sub.add_argument("part_number", type=str)

    config_subparser = config_sub.add_subparsers(
        dest="config_mode", required=True
    )
    sub_list.append(add_config := config_subparser.add_parser("add"))
    add_config.add_argument("--pdf", type=str, nargs="+", help="TODO")
    add_config.add_argument("--csv", type=str, nargs="+", help="TODO")

    sub_list.append(delete_config := config_subparser.add_parser("delete"))
    delete_config.add_argument("--pdf", type=str, nargs="+", help="TODO")
    delete_config.add_argument("--csv", type=str, nargs="+", help="TODO")

    sub_list.append(list_config := config_subparser.add_parser("list"))
    list_config.add_argument("--pdf", type=str, nargs="+", help="TODO")
    list_config.add_argument("--csv", type=str, nargs="+", help="TODO")

    for sub in sub_list:
        sub.add_argument("--rm", type=str, default="test", help="Run mode")
        sub.add_argument(
            "--verbose",
            action="store_true",
            help="Print comments as process goes on"
        )
        sub.add_argument(
            "--config",
            type=str,
            default="config.yaml",
            help="YAML file containing information for running the program",
        )
        sub.add_argument(
            "--output",
            type=str,
            default=r"./log1.txt",
            help="output path for the program",
        )
        sub.add_argument("--user", type=str, required=False)
        sub.add_argument(
            "--passkey", type=str, required=False
        )  # TODO : add comments for these

    return parser.parse_args()
