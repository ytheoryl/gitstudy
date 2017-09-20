# -*- coding: utf-8 -*-

def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x


a = input('pls input age：')
a = int(a)
b = my_abs(a)
print(b)
