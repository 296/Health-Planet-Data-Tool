#!/usr/local/bin/python3

import os
import sys
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
import datetime


@dataclass_json
@dataclass
class ExportDataElm:
    date: str
    keydata: float
    model: str
    tag: int


@dataclass_json
@dataclass
class ExportData:
    birth_date: datetime
    height: float
    sex: str
    data: List[ExportDataElm]


def main(args):
    pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ifn', type=str)
    parser.add_argument('-o', '--ofn', type=str)
    args = parser.parse_args()
    main(args)
