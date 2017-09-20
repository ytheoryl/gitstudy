# -*- coding: utf-8 -*-
import math


# my version of abs
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x


'''
a = input('pls input age：')
a = int(a)
b = my_abs(a)
print(b)
'''


# a blank function def
def nop():
    pass


def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y + step * math.sin(angle)
    return nx, ny

