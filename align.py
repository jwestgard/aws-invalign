#!/usr/bin/env python3

import sys
from zipfile import ZipFile

INPUTZIP = sys.argv[1]

# opening the zip file in READ mode
with ZipFile(INPUTZIP, 'r') as zip:
    for item in zip.infolist():
        if item.path.startswith('__MACOSX'):
            continue
        elif item.fiename
            print(file.filename)


