#/usr/bin/python3.6 is needed


line = '======================='
box = '''
--------------
|  example   |
--------------
'''

print (box)
print('I think' 'pl', 150+5, 'dollar is ok')
print ()
name = input('pls input your name:')
age = input('pls input your age:')

#int(str) transfer string to number
agenum = int(age)
if agenum >=18:
    print('_adult_')
if agenum <=12:
    print ('_child_')
else:
    print ('_teenager_')


#use "" to include ' as special symbol, or use '' to include "
# and use \ to set " as string.
print("Welcome back to \"Nokia\", I'm",name,'of',age,'!')
print (line)


