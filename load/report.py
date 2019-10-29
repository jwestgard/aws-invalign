#!/usr/bin/env python3

import csv
import os
import yaml
from inventory import Inventory


ROOT = '/home/jwestgard/Desktop/aws/data'
LIST = '../data/master_index.yml'
RESTORE = 'restored_inventories'

class Batch():

    '''Class representing a batch of inventory files'''

    def __init__(self, manifest):
        self.contents = []
        with open(manifest) as handle:
            master_list = yaml.safe_load(handle)
            for (id, dict) in master_list.items():
                files = dict.get('source')
                for file in files:
                    path = os.path.join(ROOT, file)
                    self.contents.append(Inventory(id, path))



def main():

    lookup = {}
    basedir = os.path.join(ROOT, RESTORE)
    for file in os.listdir(basedir):
        filepath = os.path.join(basedir, file)
        if os.path.isdir(filepath):
            continue
        else:
            inv = Inventory(file, filepath)
            lookup[file] = set([(a.filename, a.bytes, a.md5) for a in inv.contents])

    batch = Batch(LIST)
    outhandle = open('output.csv', 'w')
    writer = csv.writer(outhandle)
    writer.writerow(['id','bytes','assets','overlap',
                     'percent','master_file','restore_file'])
    for inv in batch.contents:
        print(f"\n{inv.batch_id}")
        print("=" * len(inv.batch_id))
        print(inv.filepath)
        print(f"Assets: {len(inv.contents)}")
        master = set([(a.filename, a.bytes, a.md5) for a in inv.contents])
        best_match = None
        for file in lookup:
            total = len(master)
            percent = 0
            intersect = master.intersection(lookup[file])
            overlap = len(intersect)
            if overlap:
                percent = (overlap / total) * 100
                percent = round(percent, 2)
                if best_match is None or percent > best_match[1]:
                    best_match = (overlap, percent, file)
                    print(f"Match: {overlap}/{total}={percent}%: {file}")

        if best_match:
            overlap, percent, restore = best_match
        else:
            overlap = 0
            percent = 0
            restore = None

        writer.writerow([inv.batch_id,
                         inv.bytes(),
                         total,
                         overlap,
                         percent,
                         os.path.basename(inv.filepath),
                         restore
                         ])


if __name__ == "__main__":
    main()
