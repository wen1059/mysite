# -*- coding: utf-8 -*-
# date: 2024-8-2
from fuzzywuzzy import process

match = process.extractOne('ahhysgh', ['ahjjsydh', '12771836', 'aiiushfg'])
print(match)
