# -*- coding: utf-8 -*-
# date: 2024-12-2
import os.path
import sys

from PyPDF4 import PdfFileMerger

merger = PdfFileMerger()
for f in sys.argv[1:]:
    merger.append(f)
with open(os.path.join(os.path.split(sys.argv[1])[0], 'merge.pdf'), 'wb') as output:
    merger.write(output)
