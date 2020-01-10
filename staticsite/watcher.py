import logging
import os
import time
from hashlib import md5

from .discovery import get_files


def get_md5(fname):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def watch(src, trigger_fn, *, interval=0.3):
    last_hsh = None
    while True:
        try:
            new_hsh = md5(
                (
                    "".join(
                        get_md5(path)
                        for path in sorted(get_files(src, src=None, skip_hidden=False))
                    )
                ).encode()
            ).hexdigest()
            if new_hsh != last_hsh:
                print("Merkel tree hash:", new_hsh, end="\r")
                trigger_fn(
                    sitehash=new_hsh, autoreload=True, check_interval=interval * 1000
                )
            last_hsh = new_hsh
        except Exception as e:
            logging.exception(e)
        finally:
            time.sleep(interval)
