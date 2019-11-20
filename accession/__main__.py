#!/usr/bin/env python3

import csv
import os
import sys

from records import AccessionRecord
from records import AccessionRecordList


def read_file(filepath):
    """
    Read the file at the provided path, attempting with various encodings and return contents as a list of lines, with newlines removed, or None if the
    file could not be read.
    """
    if os.path.isfile(filepath):
        for encoding in ['ascii', 'utf-8', 'latin-1']:
            try:
                with open(filepath, encoding=encoding) as handle:
                    lines = [line.strip('\n') for line in handle.readlines()]
                    return lines
            except ValueError:
                # File decode unsuccessful, attempt next encoding
                continue
        # If all encodings have failed to decode the file
        return None
    else:
        # If the file could not be found, or the path did not point to a file
        print(f'Could not access {filepath}')
        return None


def main():
    """
    Read the contents of each file in ROOT, listing the file and number of
    lines.
    """
    ROOT = sys.argv[1]
    files = os.listdir(ROOT)
    asset_total = 0
    error_total = 0

    with open(sys.argv[2], 'w') as outhandle:
        for file in files:
            path = os.path.join(ROOT, file)
            if file.startswith('KAP'):
                archive = 'KAP'
            else:
                archive = 'Archive' + file[7:10]
            source = file
            lines = read_file(path)
            if lines is not None:
                asset_total += len(lines)
                firstline = lines[0]

                if firstline.startswith('Volume in drive'):
                    type = 'dirlisting'
                    arlist = AccessionRecordList.from_dirlist(
                                                    lines, archive, source
                                                    )
                elif firstline.startswith('2012-03-16-digital'):
                    type = 'special'
                    arlist = AccessionRecordList.from_special(
                                                    lines, archive, source
                                                    )
                elif '\t' in firstline:
                    type = 'tab-delimited'
                    arlist = AccessionRecordList.from_csv(
                                                    lines, '\t', archive, source
                                                    )
                elif ',' in firstline:
                    type = 'comma-delimited'
                    arlist = AccessionRecordList.from_csv(
                                                    lines, ',', archive, source
                                                    )
                else:
                    type = 'unknown'

                print()
                print(f'   FILE: {file}')
                print(f'   HEAD: {firstline}')
                print(f'   TYPE: {type}')
                print(f' SOURCE: {source}')
                print(f'ARCHIVE: {archive}')
                print()

                writer = csv.writer(outhandle)
                for asset in arlist.contents:
                    writer.writerow([asset.archive, asset.source, asset.line, 
                                    asset.filename, asset.bytes, asset.timestamp,
                                    asset.md5]
                                    )

            else:
                print(f'Failed to read {file}')
                error_total += 1

    print(f'Read {asset_total} lines from {len(files)} inventory files')
    print(f'{error_total} files could not be read')


if __name__ == "__main__":
    main()
