import csv
import os
import sys


class AccessionRecord():

    '''Class representing the authoritative record of a digital asset
     under management, usually created at accession time'''

    def __init__(self, filepath):
        self.filename = os.path.basename(filepath)


class Inventory():

    '''Class representing a group of AccessionRecords'''

    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def from_dirlist(cls):

        '''Read from a basic director listing'''

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
