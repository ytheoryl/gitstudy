#!/var/bin/env python3
# -*- coding: utf-8 -*-

import math
from learn.study10_def import my_abs
from learn.study10_def import move

print(my_abs(-33))

print('*****************************************')

print('Movement in game:')
x, y = move(100, 100, 60, math.pi / 6)
print(x, y)

r = move(100, 100, 60, math.pi / 6)
print(r)
