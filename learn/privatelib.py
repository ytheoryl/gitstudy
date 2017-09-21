#!/usr/bin/env python3

import math
import subprocess


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
