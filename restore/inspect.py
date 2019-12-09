#!/usr/bin/env python3

import csv
import re
import os
import sys

LIST = sys.argv[1]
ROOT = "/Users/westgard/Box Sync/AWSMigration/aws-migration-data/RestoredFilesEnhanced"

class Asset():
    def __init__(self, md5, path, filename, bytes):
        self.md5 = md5
        self.path = path
        self.filename = filename
        self.bytes = int(bytes)


class Inventory():
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(self.path)
        with open(self.path) as handle:
            self.contents = [Asset(*row) for row in csv.reader(handle)]
        self.filecount = len(self.contents)
        self.bytecount = sum([asset.bytes for asset in self.contents])


class Batch():
    def __init__(self, phase, batch, file_path, inv_path):
        self.phase = phase
        self.name = batch
        self.file_path = file_path
        self.inv_path = inv_path


def main():
    data = {}
    with open(LIST) as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            batch = Batch(**row)
            localpath = os.path.join(ROOT, batch.inv_path)
            inv = Inventory(localpath)
            assetset = set(
                [(asset.md5, asset.filename, asset.bytes) for asset in inv.contents]
                )
            data.setdefault(batch.name, []).append(assetset)
            print(batch.name, inv.bytecount, inv.filecount)

    for batch, folders in data.items():
        print(batch)
        for folder in folders:
            print(f"  - {len(folder)}")

if __name__ == "__main__":
    main()
