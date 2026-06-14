#!/usr/bin/env python3

import argparse
from pathlib import Path
import pydantic_yaml

from inliner.config import Config, load_config
from inliner.inliner import inline

def main():
    parser = argparse.ArgumentParser(
        prog="gcs-script-inliner",
        description="Inlines functions from .js files into gcs files",
    )
    class Args():
        config: Path
        parser.add_argument("-c", "--config", type=Path, default="config.yaml")
        print_config: bool
        parser.add_argument("--print-config", type=bool, default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args(namespace=Args())
    config: Config = load_config(args.config)

    if args.print_config:
        print(pydantic_yaml.to_yaml_str(config))
        return
    
    inline(config)

if __name__ == "__main__":
    main()
