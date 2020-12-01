"""Radiant Voices code generator tool"""

import argparse
import logging
import sys
from importlib import import_module
from pathlib import Path

import genrv
import yaml
from jinja2 import Environment, FileSystemLoader, PrefixLoader
from stringcase import camelcase, pascalcase

log = logging.getLogger(__name__)


DESCRIPTION = __doc__.splitlines()[0].strip()


def arg_parser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--config",
        action="store",
        required=True,
        help="Path to genrv-config.yaml file.",
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


def enumname(ekey: str) -> str:
    ekey = str(ekey).replace("/", "_")
    ekey = ekey.replace("*", "_")
    ekey = ekey.replace(".", "_")
    if ekey[0].isdigit():
        ekey = f"{ekey[-2:].lower()}_{ekey[:2]}"
    return ekey


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("genrv").setLevel(logging.DEBUG)
    genrv_path = Path(genrv.__file__).parent
    loader_map = {
        gen_name: FileSystemLoader(genrv_path / "codegen" / gen_name)
        for gen_name in {"python", "ts"}
    }
    env = Environment(loader=PrefixLoader(loader_map))
    env.filters["camelcase"] = camelcase
    env.filters["enumname"] = enumname
    env.filters["pascalcase"] = pascalcase
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
