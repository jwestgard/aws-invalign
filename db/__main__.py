#!/usr/bin/env python3

import sqlite3
import os
import sys


class Database():

    def __init__(self, file):

        schema = '''CREATE TABLE restored (
                        id INTEGER PRIMARY KEY,
                        md5 TEXT,
                        path TEXT,
                        sourceFile TEXT,
                        sourceLine INTEGER)'''

        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(schema)


    def __del__(self):

        self.conn.commit()
        self.conn.close()


    def deposit(self, asset_tuple):

        query = '''INSERT INTO restored (md5, path, sourceFile, sourceLine)
                    VALUES (?, ?, ?, ?)'''

        self.cursor.execute(query, asset_tuple)
        self.conn.commit()


class InventoryFile():

    def __init__(self, path):

        self.invpath = path
        self.lines = []

        with open(path) as handle:
            for n, line in enumerate(handle.readlines(), 1):
                md5, path = line.strip().split(None, 1)
                file_signature = (n, md5, path, self.invpath, n)
                self.lines.append(file_signature)


class Batch():

    def __init__(self, rootdir):

        self.skipped = []
        self.inventories = []

        for file in os.listdir(rootdir):
            filepath = os.path.join(rootdir, file)
            if os.path.isfile(filepath):
                inv = InventoryFile(filepath)
                self.inventories.append(inv)
            else:
                self.skipped.append(filepath)


def main():

    db = Database('restore.db')
    batch = Batch(sys.argv[1])

    for n, inv in enumerate(batch.inventories, 1):
        header = f'({n}) {inv.invpath}: {len(inv.lines)} lines'
        print(header)
        print('=' * len(header))
        for line in inv.lines:
            print(line)


if __name__ == "__main__":
    main()
