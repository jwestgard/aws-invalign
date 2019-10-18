#!/usr/bin/env python3

import hashlib
import os
import sqlite3
import sys
import yaml


def load_config(path):
    with open(path) as handle:
        opts = yaml.safe_load(handle)
    return opts


class Inventory():

    '''Class handling various types of inventory files'''
    
    def __init__(self, path):
        self.path = path
        self.filename = os.path.basename(self.path)
        self.md5 = self.calculate_md5()
        self.bytes = os.stat(self.path).st_size

    def calculate_md5(self):
        hash = hashlib.md5()
        with open(self.path, 'rb') as handle:
            while True:
                datablock = handle.read(4096)
                hash.update(datablock)
                if not datablock:
                    break
        return hash.hexdigest()                    
            
    def parse(self):
        encodings = ['ascii', 'utf8', 'latin-1']
        for encoding in encodings:
            try:
                with open(self.path, 'r', encoding=encoding) as handle:
                    contents = handle.read()
                    self.encoding = encoding
                    return contents
            except ValueError:
                continue
        return None


class Database():

    '''Class for managing connection to sqlite database'''
    
    def __init__(self, path):
        self.path = path
        self._db_connection = sqlite3.connect(self.path)
        self._db_cur = self._db_connection.cursor()
        with open('initdb.sql') as handle:
            self._db_cur.executescript(handle.read())

    def query(self, query, params):
        return self._db_cur.execute(query, params)

    def __del__(self):
        self._db_connection.close()


class Asset():
    pass


def main():
    config = load_config(sys.argv[1])
    rootdir = config['SOURCEDIR']
    db = Database(config['DATABASE'])
    
    for file in os.listdir(rootdir):
        path = os.path.join(rootdir, file)
        inv = Inventory(path)
        inv.parse()
        print(inv.filename, inv.encoding)


if __name__ == "__main__":
    main()
