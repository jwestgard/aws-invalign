#!/usr/bin/env python3

import re
import sys

class DirList():

    def __init__(self, path):
        self.contents = []
        with open(path) as handle:
            self.lines = [line.strip() for line in handle.readlines()]

        f_pat = re.compile(
            r'(\d+)\s+File\(s\)\s+([0123456789,]+)\s+bytes'
            )
        d_pat = re.compile(
            r'(\d+)\s+Dir\(s\)\s+([0123456789,]+)\s+bytes\sfree'
            )
        e_pat = re.compile(
            r'(\d{2})/(\d{2})/(\d{4})\s+' +
            r'(\d{2}:\d{2}\s[AP]M)\s+' +
            r'([0123456789,]+)\s(.+?)$'
            )

        for n, line in enumerate(self.lines):
            match = re.match(e_pat, line)
            if match:
                month, day, year, time = match.group(1, 2, 3, 4)
                bytes = int(''.join([c for c in match.group(5) if c.isdigit()]))
                filename = match.group(6)
                self.contents.append(Asset(filename=filename, bytes=bytes))
            match = re.search(f_pat, line)
            if match:
                self.total_assets = match.group(1)
                self.total_bytes = match.group(2)
            match = re.search(d_pat, line)
            if match:
                self.total_dirs = match.group(1)

    def size(self):
        return sum([asset.bytes for asset in self.contents])


class Asset():

    def __init__(self, filename, bytes):
        self.filename = filename
        self.bytes = bytes


if __name__ == "__main__":
    dirlist = DirList(sys.argv[1])
    print("Total assets/bytes:", len(dirlist.contents), dirlist.size())
    print("Reported assets:", dirlist.total_assets)
    print("Reported bytes:", dirlist.total_bytes)
