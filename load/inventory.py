import csv

excl = ['.DS_Store', 'Extension -', 'Total file size']

class Inventory():

    def __init__(self, batch_id, filepath):
        self.batch_id = batch_id
        self.filepath = filepath
        self.contents = self.read_file()

    def read_file(self):
        contents = []
        encodings = ['ascii', 'utf8', 'latin-1']
        for encoding in encodings:
            try:
                with open(self.filepath, encoding=encoding) as handle:
                    data = handle.readlines()
                    break
            except ValueError:
                continue

        header_line = data[0]
        if header_line.startswith(" "):
            pass
        else:
            if '\t' in header_line:
                separator = '\t'
            else:
                separator = ','
            reader = csv.DictReader(data, delimiter=separator)
            for row in reader:
                if 'Type' in row:
                    if row['Type'] != 'File':
                        continue
                a = Asset(row)
                if a.filename is None or any([a.filename.startswith(e) for e in excl]):
                    continue
                else:
                    contents.append(a)
        return contents

    def bytes(self):
        return sum([asset.bytes for asset in self.contents if asset.bytes is not None])



class Asset():

    def __init__(self, row):
        attributes = [('filename', ['Filename', 'FILENAME', 'File Name', 'Key']),
                     ('bytes', ['Bytes', 'BYTES', 'File Size', 'Size']),
                     ('md5', ['MD5', 'md5', 'Other', 'Data'])]

        for (name, keys) in attributes:
            for key in keys:
                if key in row:
                    if name == 'bytes':
                        if row[key] is not None:
                            try:
                                setattr(self, name, int(row[key]))
                            except ValueError:
                                setattr(self, name, row[key])
                                print(row[key])
                        else:
                            setattr(self, name, 0)
                    else:
                        setattr(self, name, row[key])
                else:
                    continue
            if not hasattr(self, name):
                setattr(self, name, None)
