import argparse

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

args = parser.parse_args()
if args.cmd == "build":
    build(src=args.src, target=args.target)
elif args.cmd == "watch":

    def on_change(**variables):
        build(src=args.src, target=args.target, variables=variables)

    watch(args.src, on_change)
