#!/usr/bin/env python3

import os
import sys


def read_file(filepath):
    '''Attempt to read the file path using various encodings and return
        file contents'''
    if not os.path.isfile(filepath):
        print(f'Could not access {filepath}')
        return None
    else:
        for encoding in ['ascii', 'utf-8', 'latin-1']:
            try:
                with open(filepath, encoding=encoding) as handle:
                    contents = [line.strip() for line in handle.readlines()]
                    return contents
            except ValueError:
                continue
        return None


def main():

    ROOT = sys.argv[1]
    files = os.listdir(ROOT)
    asset_total = 0
    error_total = 0

    for file in files:
        path = os.path.join(ROOT, file)
        contents = read_file(path)
        if contents is not None:
            print(file, len(contents))
            asset_total += len(contents)
        else:
            print(f'Failed to read {file}')
            error_total += 1

    print(f'Read {asset_total} lines from {len(files)} inventory files')
    print(f'{error_total} files could not be read')

if __name__ == "__main__":
    main()
