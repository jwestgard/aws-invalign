#!/usr/bin/env python3

import re
import os
import sys

ROOT = sys.argv[1]

class Inventory():
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(self.path)
        with open(self.path) as handle:
            self.contents = [line.strip() for line in handle.readlines()]
        self.filecount = len(self.contents)
        self.bytecount = 0
        for line in self.contents:
            cols = line.split(',')
            self.bytecount += int(cols[3])


def main():
    for file in os.listdir(ROOT):
        path = os.path.join(ROOT, file)
        inv = Inventory(path)
        print(inv.filename, inv.filecount, inv.bytecount)

if __name__ == "__main__":
    main()
