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
b = a  # b has the same value as a
a = 'XYZ'  # given a a new value, b still has the old value
print(a, b)
print(line)

print(10 / 3)  # 正常除法带小数
print(10 // 3)  # 地板除，没有余数
print(10 % 3)  # 显示余数
