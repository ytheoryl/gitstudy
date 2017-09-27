#!/usr/bin/env python3
# -*- coding:utf-8 -*-

moneyratiodict = {'YUEBAO': 0.04, 'WANGSHANG': 0.0415, 'ZHEN': 0.0554,
                  'ZHEN30': 0.065, 'ZHEN90': 0.075, 'ZHEN365': 0.085}

for x, y in moneyratiodict.items():
    print('%s年化收益是%s%%' % (x, y*100))

total = float(input('your total investment:'))


def allin(u, i):
    income = total * i
    incomem = income / 12
    incomed = income / 365
    print('The income of %9s| \t%.2f\t%.2f\t%.2f' % (u, income, incomem, incomed))
    print('------------------------------------------------')


print('''
------------------------------------------------
                            YEAR    MONTH   DAY
================================================
''')

for x, y in moneyratiodict.items():
    allin(x, y)

# another output format:


def another(u, i):
    inc = total * i
    return '%.2f' % inc  # 把返回值变为2位小数


LL = []
for x, y in moneyratiodict.items():
    LL.append((another(x, y)))
for i in LL:
    print(i)

#print('the year of them are %s' % )
