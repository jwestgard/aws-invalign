#!/usr/bin/env python3

from .inventory import Inventory
import os
import sys
import yaml


def read_yaml(path):
    with open(path) as handle:
        results = yaml.safe_load(handle)
    return results


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

    config = read_yaml(sys.argv[1])

    MANIFEST  = config['MANIFEST']
    INPUTZIP  = config['INPUTZIP']
    SOURCEDIR = config['SOURCEDIR']
    TARGETDIR = config['TARGETDIR']
    REQUESTS  = sys.argv[2:] or config['REQUESTS']

    with open(MANIFEST) as handle:
        manifest = yaml.safe_load(handle)

    for request in REQUESTS:
        if request not in manifest:
            print(f'Found no entries for "{request}" in the manifest')
        else:
            requested_archive = manifest.get(request)
            source = requested_archive['source']
            target = requested_archive['target']

            print(request.upper())
            print('=' * len(request))
            print("Source:", source)
            print("Target:", target)

            for file in source:
                path = os.path.join(SOURCEDIR, file)
                inv = Inventory(path)
                inv.from_dirlist()
                print(f'Inventory contains {len(inv.assets)} assets')


if __name__ == "__main__":
    main()
