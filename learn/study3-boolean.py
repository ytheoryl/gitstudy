box = '''
##############
#  example   #
##############
'''
line = '======================='
print(box)

# boolean
print(3 < 8)
print(1+1 < 2)

really = 2*4 > 1
# , will generate a space
print('\n', really)
print(line)
print('__Boolean Calculation__')
# and=both True, or=one True, not
a = 5 > 3  # True
b = 3 > 5  # False
c = 2*5 == 10  # True
print(a and b)
print(a or b)
print(c and a)
print(line)

a = 'ABC'
b = a
a = 'XYZ'
print(a, b)
print(line)

print(10 / 3)
print(10 // 3)
print(10 % 3)
