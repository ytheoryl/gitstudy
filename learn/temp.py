#!/var/bin/env python3
# -*- coding: utf-8 -*-

import math
import os
from learn.study10_def import my_abs
from learn.study10_def import move
from learn.privatelib import exec_shell

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

print('*****************')
os.system('cat /proc/cpuinfo | grep model > /home/leo/Documents/cpu.txt')
#os.system('echo '' > /home/leo/Documents/cpu.txt')

run = exec_shell('cat /home/leo/Documents/cpu.txt')
print(run)
exec_shell('echo '' > /home/leo/1Documents/cpu.txt')

