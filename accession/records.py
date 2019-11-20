import csv
import os
import sys


class AccessionRecord():
    """
    Class representing the authoritative record of a digital asset
    under management, usually created at accession time.
    """

    def __init__(self, filename, bytes, timestamp, md5, archive, source, line):
        self.filename = filename
        self.bytes = bytes
        self.timestamp = timestamp
        self.md5 = md5
        self.archive = archive
        self.source = source
        self.line = line


class AccessionRecordList():
    """
    Class representing a group of AccessionRecords.
    """

    def __init__(self, contents):
        self.contents = contents

    @classmethod
    def from_dirlist(cls, lines, archive, source):
        '''Read assets from a basic directory listing.'''
        assets = []
        for n, line in enumerate(lines):
            if line == '' or line.startswith(' '):
                continue
            parts = line.split()
            print(parts)
            length = len(parts)
            if length == 0 or parts[3] == '<DIR>':
                continue
            elif length >= 5:
                timestamp = ' '.join(parts[:3])
                bytes = int(''.join(
                    [char for char in parts[3] if char.isdigit()]
                    ))
                filename = ' '.join(parts[4:])
                assets.append(
                    AccessionRecord(filename, bytes, timestamp, md5, archive, source, n)
                    )
        return cls(assets)

    @classmethod
    def from_special(cls, lines, archive, source):
        '''Read special dirlist format.'''
        assets = []
        for n, line in enumerate(lines):
            if line.startswith(' '):
                parts = line.split('\t')
                filename = parts[0].strip()
                val, units = parts[2].strip().split()
                if units == 'MB':
                    bytes = int(round(float(val) * 1024 * 1024))
                else:
                    bytes = None
                timestamp = parts[4].strip()
                md5 = None
                assets.append(
                    AccessionRecord(filename, bytes, timestamp, md5, archive, source, n)
                    )
        return cls(assets)

    @classmethod
    def from_csv(cls, lines, delimiter, archive, source):
        '''Read assets from a CSV file.'''
        assets = []
        reader = csv.DictReader(lines, delimiter=delimiter)
        for n, row in enumerate(reader):
            bytes = None
            timestamp = None
            md5 = None
            for key in ['Filename', 'FILENAME', 'File Name', 'Key']:
                if key in row:
                    filename = row[key]
                    break
                else:
                    continue
            for key in ['Bytes', 'BYTES', 'File Size', 'Size']:
                if key in row:
                    bytes = row[key]
                    break
                else:
                    continue
            for key in ['Mtime', 'MTime', 'MTIME', 'Mod Date', 'Date']:
                if key in row:
                    timestamp = row[key]
                    break
                else:
                    continue
            for key in ['MD5', 'md5', 'Data', 'Other']:
                if key in row:
                    md5 = row[key]
                    break
                else:
                    continue
            assets.append(
                AccessionRecord(filename, bytes, timestamp, md5, archive, source, n)
                )
        return cls(assets)

