#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-

height = input('pls input your height(m):')
weight = input('pls input your weight(kg):')
bmi = float(weight) / (float(height) ** 2)

if bmi < 18.5:
    result = '过轻'
elif bmi < 25:
    result = '正常'
elif bmi < 28:
    result = '过重'
elif bmi < 32:
    result = '肥胖'
else:
    result = '严重肥胖'

print('你的BMI是%.2f, 属于：%s' % (bmi, result))
