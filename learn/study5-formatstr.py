# -*- coding: utf-8 -*-
line = '#################'

# %s字符 %f浮点数 %d整数 %x十六进制整数
print('Hello, %s' % 'world')
print('Hello, %s is %s' % ('world', 'ok'))
# 1000.99被%d取整, %.2f指定小数点位数
print('Hello %s, you have $%d and $%.2f bonus!' % ('Leo', 99.12345, 99.12345))
print(line)

# the 5 below means %d starting from 5th (4 spaces before)
print('%5d+%d' % (3, 62))
print(line)

a = 72
b = 85
c = (b - a) / a * 100
print('the improvement is %.1f%s ' % (c, '%'))
