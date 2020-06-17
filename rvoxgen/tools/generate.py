"""Radiant Voices code generator tool"""

import argparse
from importlib import import_module
import logging
from pathlib import Path
import sys

import yaml
from jinja2 import Environment, PrefixLoader, FileSystemLoader

import rvoxgen

log = logging.getLogger(__name__)


DESCRIPTION = __doc__.splitlines()[0].strip()


def arg_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--config",
        action="store",
        required=True,
        help="Path to config.yaml file containing multiple configurations to generate.",
    )
    return parser


def resolve_object_name(objname):
    modname, attrname = objname.split(":")
    obj = import_module(modname)
    for part in attrname.split("."):
        obj = getattr(obj, part)
    return obj


def generate(env, generator, **options):
    cls = resolve_object_name(generator)
    codegen = cls(**options)
    log.info("Running codegen %r", codegen)
    codegen.run(env)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("rvoxgen").setLevel(logging.DEBUG)
    rvoxgen_path = Path(rvoxgen.__file__).parent
    loader_map = {
        gen_name: FileSystemLoader(rvoxgen_path / gen_name)
        for gen_name in {"pymutable", "pyimmutable", "jsmutable", "jsimmutable"}
    }
    env = Environment(loader=PrefixLoader(loader_map))
    env.filters["repr"] = repr
    parser = arg_parser()
    options = parser.parse_args()
    config_path = Path(options.config)
    with config_path.open() as f:
        configs = yaml.safe_load(f)
    for config in configs:
        log.info(f"Generating code with {config['generator']}...")
        generate(env, **config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
