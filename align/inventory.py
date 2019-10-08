import csv
from io import StringIO
import sys
import yaml
from zipfile import ZipFile


class Inventory():

    def __init__(self, filename, ziparchive):
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


    def read_data(self):

        if self.type == 'dirlist':
            lines = [
                line.strip('\n') for line in StringIO(self.text).readlines()
                ]
            entries = [line for line in lines if not line.startswith(' ')]
            for entry in entries:
                parts = entry.split()
                length = len(parts)
                if length == 0 or parts[3] == '<DIR>':
                    continue
                elif length >= 5:
                    timestamp = ' '.join(parts[:3])
                    bytes = int(''.join(
                        [char for char in parts[3] if char.isdigit()]
                        ))
                    filename = ' '.join(parts[4:])
                else:
                    print('non-standard line format')
                    continue
                result = (filename, bytes, timestamp)
                print(result)
