#/usr/bin/python3.6 is needed


line = '======================='
box = '''
--------------
|  example   |
--------------
'''

print (box)
print('I think' 'pl', 150+5, 'dollar is ok')
name = input('pls input your name:')
age = input('pls input your age:')
#use "" to include ' as special symbol. and use \ to set " as string.
print("Welcome back to \"Nokia\", I'm",name,'of',age,'!')
print (line)
print ()

print (box)
result = 1024*768
#\n\t are string, \n means a new line, \t means a table
print ("1024 * 768 =\n\t",-result)

#print a \, a new line, and a \
print ('\\\n\\')
#use r" to ignore \
print (r'\\\n\\')
#\r means an 'return' at current line
print ('abc\rdef')