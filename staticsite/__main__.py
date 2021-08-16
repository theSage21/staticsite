import argparse
import importlib

import yaml

from .builder import build
from .watcher import watch

parser = argparse.ArgumentParser(
    prog="python -m staticsite",
    description=(
        "A super simple static site generator using Jinja2. The folder structure of "
        "the source is preserved.Files starting with `.` are ignored."
    ),
)
parser.add_argument("--src", default="src")
parser.add_argument("--target", default="www")
parser.add_argument(
    "cmd",
    default="build",
    choices=["build", "watch"],
    help="What action do you want to take? "
    "Build will simply compile the static site into the target directory "
    "while watch will re-build the site any time the source changes and reload the browser when it does.",
)
parser.add_argument(
    "--config",
    default=None,
    help="The variables in this file are made available to the templates."
    " You can use this to set things like the base url for your site.",
)

args = parser.parse_args()


def get_config(fl):
    config = yaml.load(fl, Loader=yaml.FullLoader)
    plugs = {}
    if "plugins" in config:
        for key, value in config["plugins"].items():
            *mod, fn = value.split(".")
            plugs[key] = getattr(importlib.import_module(".".join(mod)), fn)
    config["plugins"] = plugs
    return config


for path in [args.config, "staticsite.yaml", "staticsite.yml"]:
    if path is None:
        continue
    try:
        with open(path, "r") as fl:
            config = get_config(fl)
        break
    except FileNotFoundError as e:
        raise e
        config = {"plugins": {}}


if args.cmd == "build":
    build(src=args.src, target=args.target, config=config)
elif args.cmd == "watch":

    def on_change(**variables):
        build(src=args.src, target=args.target, variables=variables, config=config)

    watch(args.src, on_change)
