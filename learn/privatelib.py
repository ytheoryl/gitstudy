#!/usr/bin/env python3

import math
import subprocess  # subprocess replaced commands


def exec_shell(cmd):
    ret = subprocess.getstatusoutput(cmd)
    if ret[0]:
        raise Exception('status: %s; output: %s' % (ret[0], ret[1]))
    return ret


def nop():
    pass


def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y + step * math.sin(angle)
    return nx, ny


def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
