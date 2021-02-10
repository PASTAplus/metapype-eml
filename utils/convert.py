#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: convert

:Synopsis:

:Author:
    servilla

:Created:
    2/9/21
"""
from datetime import date
import json
import logging
import os
from pathlib import Path

import click
import daiquiri


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/convert.log"
daiquiri.setup(level=logging.INFO,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)


def to_20210209(model: dict):
    for node in model:
        model[node].insert(1, {"nsmap": {}})
        model[node].insert(2, {"prefix": None})
        model[node].insert(4, {"extras": {}})
        model[node].insert(6, {"tail": None})
        children = model[node][7]["children"]
        for child in children:
            to_20210209(child)


recursive_help = "Recursively convert json files; requires 'path' be a directory"
overwrite_help = "Overwrite JSON file(s) in place; otherwise make obvious copy"
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("json_path", nargs=1, required=True)
@click.option("-r", "--recursive", is_flag=True, default=False, help=recursive_help)
@click.option("-o", "--overwrite", is_flag=True, default=False, help=overwrite_help)
def main(json_path: str, recursive: bool, overwrite: bool):
    """
        Convert current Metapype JSON format to latest JSON format

        \b
            JSON_PATH: file system path to single JSON file or directory of JSON file(s)
    """
    jp = Path(json_path)
    if not jp.exists:
        msg = f"'{json_path}' does not exist"
        raise IOError(msg)
    else:
        json_files = list()
        if jp.is_file():
            if jp.suffix == ".json":
                json_files.append(json_path)
            else:
                msg = f"'{jp.name}' is not with 'json' extension"
                raise IOError(msg)
        elif recursive:
            json_files = [_ for _ in jp.glob("**/*.json")]
        else:
            json_files = [_ for _ in jp.glob("*.json")]

    for json_file in json_files:
        with open(json_file, "r") as f:
            model = json.loads(f.read())
        to_20210209(model)
        if not overwrite:
            ext = date.today().strftime("%Y%m%d")
            if Path(f"{json_file}.{ext}").exists():
                msg = f"Previous version '{json_file}.{ext}' alread exists"
                raise IOError(msg)
            Path(json_file).replace(f"{json_file}.{ext}")
        with open(json_file, "w") as f:
            f.write(json.dumps(model, indent=2))

    return 0


if __name__ == "__main__":
    main()
