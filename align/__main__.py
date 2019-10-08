#!/usr/bin/env python3

import csv
from .inventory import Inventory
from io import StringIO
import sys
import yaml
from zipfile import ZipFile


def read_zip_archive(path):

    '''Inspect a ZIP archive and read data from it'''

    with ZipFile(INPUTZIP, 'r') as zip:
        for item in zip.infolist():
            if item.path.startswith('__MACOSX'):
                continue
            elif item.fiename:
                print(file.filename)


def main():

    '''Main program logic goes here'''

    MANIFEST = sys.argv[1]
    INPUTZIP = sys.argv[2]
    ARCHIVE  = sys.argv[3]

    with open(MANIFEST) as handle:
        data = yaml.safe_load(handle)

    inventories = data.get(ARCHIVE)

    if not inventories:
        print(f'Found no entries for "{ARCHIVE}" in the master list')
    else:
        print(ARCHIVE.upper())
        for (n, filename) in enumerate(inventories, 1):
            inv = Inventory(filename, INPUTZIP)
            print(f'  ({n}) {filename} (type: {inv.type})')

            inv.read_data()


if __name__ == "__main__":
    main()
