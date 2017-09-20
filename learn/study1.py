# /usr/bin/python3.6 is needed

from learn. import my_abs

line = '======================='
box = '''
--------------
|  example   |
--------------
'''

print(box)
print('I think''spacetest', 150+5, 'dollar is ok')
print()
name = input('pls input your name:')
age = input('pls input your age:')

# len() is used to calcuate lenghth
namenum = len(name)
print('your name length is', namenum, 'digits')

# int(str) transfer string to number
agenum = int(age)
agenum = my_abs(agenum)

if agenum >= 80:
    print('_really?_')
elif agenum >= 18:
    print('_adult_')
elif agenum <= 6:
    print('_child_')
else:
    print('_teenager_')


# use "" to include ' as special symbol, or use '' to include "
# and use \ to set " as string.
print("Welcome back to \"Nokia\", I'm", name, 'of', age, '!')
print("Welcome back to \"Nokia\", I'm %s of %d!" % (name, agenum))
print(line)
print('\tline length is', len(line), 'digits')
