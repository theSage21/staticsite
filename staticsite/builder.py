import os
import shutil

from flask_minify import decorators
from jinja2 import Environment, FileSystemLoader, Template

from .discovery import get_files


def minify(html):
    @decorators.minify(html=True, js=True, cssless=True)
    def fn():
        return html

    return fn()


def build(
    src,
    target,
    files=None,
    *,
    endswith_whitelist=("html", "css", "js"),
    sitehash_path=".sitehash.txt",
    variables=None,
    config=None
):
    """
    Build "files" from "src" to "target".
    If "files" is None, build everything in "src".
    """

    def walk(folder):
        return [i for i in get_files(os.path.join(src, folder), src)]

    env = Environment(loader=FileSystemLoader(src))
    env.globals["walk"] = walk
    env.globals["site_hash_path"] = sitehash_path
    if variables is not None:
        env.globals.update(variables)
    if config is not None:
        env.globals.update(config)
    for template_path in get_files(src, src):
        target_path = os.path.join(target, template_path)
        target_dirname = os.path.dirname(target_path)
        if not os.path.exists(target_dirname):
            os.makedirs(target_dirname, exist_ok=True)
        if any(template_path.endswith(ext) for ext in endswith_whitelist):
            template = env.get_template(template_path)
            html = template.render()
            html = minify(html)
            with open(target_path, "w") as fl:
                fl.write(html)
        else:
            shutil.copy(os.path.join(src, template_path), target_path)
        if variables is not None and variables.get("sitehash") is not None:
            path = os.path.join(target, sitehash_path)
            with open(path, "w") as fl:
                fl.write(variables["sitehash"])
