#!/usr/bin/env python3
# -*- coding:utf-8 -*-

height = input('输入你的身高(米):')
weight = input('输入你的体重(公斤):')
bmi = float(weight) / (float(height) ** 2)

if bmi < 18.5:
    result = '过轻[<18.5]'
elif bmi < 25:
    result = '正常[18.5~25]'
elif bmi < 28:
    result = '过重[25~28]'
elif bmi < 32:
    result = '肥胖[28~32]'
else:
    result = '严重肥胖[>32]'

print('你的BMI是%.2f, 属于：%s' % (bmi, result))
