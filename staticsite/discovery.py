import os


def get_files(root, src=None, *, skip_hidden=True, endswith_blacklist=(".swp", "~")):
    """
    root is the folder currently being walked
    src  is the where the paths are being relatively calculated from
    """
    paths = [os.path.join(root, f) for f in os.listdir(root)]
    for path in paths:
        if (not skip_hidden) or (not os.path.basename(path).startswith(".")):
            if os.path.isdir(path):
                yield from get_files(path, src)
            else:
                if not any(path.endswith(ext) for ext in endswith_blacklist):
                    yield os.path.relpath(path, src) if src is not None else path
