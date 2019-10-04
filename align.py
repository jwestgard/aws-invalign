#!/usr/bin/env python3

INPUT = '/Users/westgard/Box Sync/DPI Projects/DigitalPreservation/aws_migration/data/original_inventories/Archive001_2010-07-27_bnafilelist.txt'

with open(INPUT) as handle:
    for line in handle.readlines():
        if line.startswith(' ') or line == '\n':
            continue
        else:
            row = line.strip('\n')
            print(row.split())
