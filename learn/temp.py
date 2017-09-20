#!/var/bin/env python3
# -*- coding: utf-8 -*-

import math
from learn.study10_def import my_abs
from learn.study10_def import move

my_abs(55)

x = 'ad'
if isinstance(x, int):
    print('ok')
else:
    print('nok')

x, y = move(100, 100, 60, math.pi / 6)
print(x, y)

r = move(100, 100, 60, math.pi / 6)
print(r)
