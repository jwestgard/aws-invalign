import csv
from io import StringIO
from zipfile import ZipFile
import os


class Inventory():

    '''Class representing an inventory of assets,
       with option to read from various file formats'''

    def __init__(self, path):
        self.path = path
        self.reachable = os.path.isfile(path)
        if self.reachable:
            with open(path) as handle:
                self.contents = handle.read()
        else:
            print(f'Could not access {self.path}')


    def from_zipfile(self, filename, ziparchive):
        with ZipFile(ziparchive) as source:
            with source.open(filename) as handle:
                self.bytes = handle.read()
                try:
                    self.text = self.bytes.decode('utf-8')
                except UnicodeDecodeError:
                    self.text = self.bytes.decode('windows-1252')
        if self.text.startswith(' Volume in drive'):
            self.type = 'dirlist'
        else:
            self.type = 'csv'


    def from_csv(self):
        pass


    def from_dirlist(self):
        self.assets = []
        for line in StringIO(self.contents).readlines():
            if line.startswith(' '):
                continue
            parts = line.strip('\n').split()
            length = len(parts)
            if length == 0 or parts[3] == '<DIR>':
                continue
            elif length >= 5:
                timestamp = ' '.join(parts[:3])
                bytes = int(''.join(
                    [char for char in parts[3] if char.isdigit()]
                    ))
                filename = ' '.join(parts[4:])
                self.assets.append((filename, bytes, timestamp))
