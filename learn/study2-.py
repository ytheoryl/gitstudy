box = '''
--------------
|  example   |
--------------
'''

print(box)
result = 1024*768
# \n\t are string, \n means a new line, \t means a table, \a is a beep sound
print("1024 * 768 =\n\t", -result, '\n\a')

# print a \, a new line, and a \
print('\\\n\\', '\n')
# use r" to ignore \
print(r'\\\n\\')
print()
# \r means an 'return' at current line
print('abc\rdef')

print('''line1
line2
line3''')
