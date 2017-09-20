#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-

YUEBAO = 0.04
WANGSHANG = 0.0415
ZHENRONGBAO = 0.0554
ZHENRONGBAO30 = 0.065
ZHENRONGBAO90 = 0.075
ZHENRONGBAO365 = 0.085

moneyratiodict = {'id1': 'YUEBAO', 'id1-1': 0.04,
              'id2': 'WANGSHANG', 'id2-1': 0.0415,
              'id3': 'ZHENRONGBAO', 'id3-1': 0.0554
}

income = 0

#moneyratio = [YUEBAO, WANGSHANG, ZHENRONGBAO, ZHENRONGBAO30, ZHENRONGBAO90, ZHENRONGBAO365]
moneyratio = [YUEBAO, WANGSHANG, ZHENRONGBAO]
moneyrationame = ('YUEBAO', 'WANGSHANG', 'ZHENGRONGBAO')

for i in moneyratio:
    print(i)

total = float(input('pls inpur your total money:'))

yearly = total
quaterly = yearly / 4
monthly = yearly / 12
daily = yearly / 365
timeframe = [yearly, quaterly, monthly, daily]
timeframeid = ('yearly', 'quaterly')

for n in timeframe:
    for x in timeframeid:
        print('===%s===' % timeframeid[0])
    for i in moneyratio:
        income = n * i
    for y in moneyrationame:
        print('%s %.2f' % (y, income))



