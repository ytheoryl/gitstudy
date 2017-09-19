#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

line = '##############'

# ord转换字符为UNICODE编码
print(ord('a'))
print(ord('网'))

print(line)

# chr转换UNICODE编码为字符
print(chr(97))
print(chr(32593))

print(line)

print('ABC'.encode('ascii'))   # 每个英文字母对应一个byte
print('\t-->bytes length in ASCII is', len(b'ABC'))
print('编程'.encode('utf-8'))  # 每个中文字符在UTF-8编码里通常占3个byte
print('\t-->bytes length in UTF-8 is', len('编程'.encode('utf-8')))
# print('编程'.encode('ascii'))  # ASCII不支持中文编码，会报错

print(line)

chineseword = b'\xe7\xbc\x96\xe7\xa8\x8b'.decode('utf-8')
print('the received bytes', r'(\xe7\xbc\x96\xe7\xa8\x8b)', 'means', '%s' % (chineseword))

print(line)

print('In UTF-8, 中 is', len('中'.encode('utf-8')), 'bytes.')
print('In GB2312, 中 is %s bytes.' % (len('中'.encode('gb2312'))))

print(line)

name1 = '中'
name2 = name1
namecode = name1.encode('gb2312')
print('namecode:', namecode)

newname = name2.encode('utf-8')
print('newname: ', newname)

longer = len(namecode) > len(newname)  # check with code is longer
print('GB2312 is longer than UTF-8:', longer)
