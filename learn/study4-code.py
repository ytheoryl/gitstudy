print(ord('A'))
print(ord('a'))
print(ord('网'))

print()

print(chr(97))
print(chr(32593))

print()

print('ABC'.encode('ascii'))   # 每个英文字母对应一个byte
print('\t-->length is', len(b'ABC'))
print('编程'.encode('utf-8'))  # 每个中文字符在UTF-8编码里通常占3个byte
print('\t-->length is', len('编程'.encode('utf-8')))
# print('编程'.encode('ascii'))  # ASCII不支持中文编码，会报错

print()

chineseword = b'\xe7\xbc\x96\xe7\xa8\x8b'.decode('utf-8')
print('the received bytes', r"(\xe7\xbc\x96\xe7\xa8\x8b)", 'means', chineseword)

print()

print('In UTF-8, 中 is', len('中'.encode('utf-8')), 'bytes.')
print('In GB2312, 中 is', len('中'.encode('gb2312')), 'bytes.')
