import argparse

import yaml

from .builder import build
from .watcher import watch

parser = argparse.ArgumentParser(
    description=(
        "Helper functions to build a static site. Folder structure of"
        "the source is preserved.Files starting with `.` are ignored."
    )
)
parser.add_argument(
    "cmd",
    default="build",
    choices=["build", "watch"],
    help="What action do you want to take?",
)
parser.add_argument("--src", default="src")
parser.add_argument("--target", default="docs")
parser.add_argument("--config", default="staticsite.yaml")

args = parser.parse_args()
with open(args.config, "r") as fl:
    config = yaml.load(fl, Loader=yaml.FullLoader)
    print(config)
if args.cmd == "build":
    build(src=args.src, target=args.target, config=config)
elif args.cmd == "watch":

    def on_change(**variables):
        build(src=args.src, target=args.target, variables=variables, config=config)

    watch(args.src, on_change)
