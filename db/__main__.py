#!/usr/bin/env python3

import sqlite3
import os
import sys

from .database import Database
from .inventory import Inventory


class Batch():

    def __init__(self, rootdir):

        self.skipped = []
        self.inventories = []

        for file in os.listdir(rootdir):
            filepath = os.path.join(rootdir, file)
            if os.path.isfile(filepath):
                inv = Inventory(filepath)
                self.inventories.append(inv)
            else:
                self.skipped.append(filepath)


def main():

    INV_ROOT = sys.argv[1]
    if len(sys.argv) == 3:
        DATABASE = sys.argv[2]
    else:
        DATABASE = ':memory:'

    db = Database(DATABASE)
    batch = Batch(INV_ROOT)

    for n, inv in enumerate(batch.inventories, 1):
        header = f'({n}) {inv.filename}: {len(inv.lines)} lines'
        print(header)
        print('=' * len(header))
        for line in inv.lines:
            db.deposit(line)

if __name__ == "__main__":
    main()
