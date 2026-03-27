import json
from typing import Optional
from argparse import Namespace
from argparse import ArgumentParser
from spark.configlib.config_loader import load_and_parse_config


def job_args_utils(extra_args: Optional[list[dict]] = None) -> Namespace:
    """
        Parse job arguments then transfer config to code
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--job_config", 
        help="Path to job config file.",
        default="",
        type=str, 
        required=True
    )

    args = parser.parse_args()

    if args.job_config != "":
        parsed_job_config = load_and_parse_config(args.job_config, args) # RETURN CONFIG OBJECT
        args.job_config = parsed_job_config

    if args.meta_config != "":
        parsed_meta_config = load_and_parse_config(args.meta_config, args)
        args.meta_config = parsed_meta_config
    return args
