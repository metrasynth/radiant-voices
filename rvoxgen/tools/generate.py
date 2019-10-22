"""Radiant Voices code generator tool"""

import argparse
from importlib import import_module
import logging
from pathlib import Path
import sys

import yaml


log = logging.getLogger(__name__)


DESCRIPTION = __doc__.splitlines()[0].strip()


def arg_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--config",
        action="store",
        help="Path to config.yaml file containing multiple configurations to generate.",
    )
    parser.add_argument(
        "--generator",
        action="store",
        help="The module name and class name of the code generator.",
    )
    return parser


def resolve_object_name(objname):
    modname, attrname = objname.split(":")
    obj = import_module(modname)
    for part in attrname.split("."):
        obj = getattr(obj, part)
    return obj


def generate(generator):
    cls = resolve_object_name(generator)
    codegen = cls()
    print(codegen)


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = arg_parser()
    options = parser.parse_args()
    if options.config and options.generator:
        log.warning("--config was specified; --generator will be ignored")
    if not options.config and not options.generator:
        log.error("--config not specified; must provide --config or --generator")
        return 1
    if options.config:
        config_path = Path(options.config)
        with config_path.open() as f:
            configs = yaml.safe_load(f)
    else:
        configs = [{"generator": options.generator}]
    for config in configs:
        log.info(f"Generating code with {config['generator']}...")
        generate(**config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
