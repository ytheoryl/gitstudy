#!/var/bin/env python3
# -*- coding: utf-8 -*-

import math

# ax^2+bx+c=0
# ax^2+c=0
# x^2 = -c/a
# y = -c/a
# x = math.sqrt(y)


def quadratic(a, c):
    if not isinstance(a,(int)):
        raise TypeError('only support int')

    y = (c / a)
    x = math.sqrt(y)
    return -x

print(math.sqrt(9))

result = quadratic(1.2, 400)
print(result)
