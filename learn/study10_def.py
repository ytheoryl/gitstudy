# -*- coding: utf-8 -*-
import math


# my version of abs
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x


'''
a = input('pls input age：')
a = int(a)
b = my_abs(a)
print(b)
'''


# a blank function def
def nop():
    pass


def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y + step * math.sin(angle)
    return nx, ny

# 位置参数
def power(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s


print(power(2, 6))


def power1(x, n=2):  # n作为默认参数，如果调用函数的时候不输入，就使用默认参数，如果加入了参数，就以参数为准
    x = x ** n
    return x


print(power1(5))
print(power1(2, 3))
print('*************************')


# 默认参数，报名表，设定一些默认值
def school(name, gender, age=6, city='Chengdu'):
    if gender == 'male':
        gender = 'male  '  # 为了显示排版整洁，把male和female对齐，增加了2个空格
    if not isinstance(age, int):
        raise TypeError('age should be int.')
    print('Name:', name, '\t\v',
          'Age:', age, '\t\v',
          'Gender:', gender, '\t\v',
          'City:', city, '\t\v'
          )


school('Li', age=11, gender='female')
school('Leo', 'male', 15, 'shanghai')
school('Ann', 'female', city='Beijing')
print('*************************')


# 如果默认参数指向一个可变的内容，在多次执行默认参数的时候，被指向的内容会不断的累加。如果带参数的引用，不影响。
def add_end(li=[]):
    li.append('END')
    return li


print(add_end([1, 2, 3]))
print(add_end([1, 2, 3]))
print(add_end(['a', 'b', 'c']))
print(add_end())
print(add_end())
print(add_end())


# 解决方法是默认参数指向到NONE。如果不带参数的引用，会先把默认值重置为空list，这样即使重复执行默认参数，也不会累加。
def add_end1(lo=None):
    if lo is None:
        lo = []
    lo.append('END')
    return lo


print(add_end1([1, 2]))
print(add_end1())
print(add_end1())


print('*************************')

# 可变参数
# given a,b,c。。。 to calculate a^2+b^2+c^2。。。数字数量不定，默认接收list或者tuple
def calc(numbers):
    he = 0
    for n in numbers:
        he = he + n * n
    return he


# 因为参数numbers接受一个对象，所以不能单独输入多个数字，只能通过list和tuple作为输入
print(calc([1,2,3]))
print(calc((1,3,2)))
#print(calc())  此时不能带空参数

# 可变参数，加上星号。既可以接收list，也可以接收数字
def calc1(*numbers):
    he = 0
    for n in numbers:
        he = he + n * n
    return he


print(calc1())  # 可变参数的时候，可以带空参数
print(calc1(2,4,3,2))
tup1 = (2,3,4,2)
print(calc1(*tup1))  # 带*可以直接把list和tuple带入函数
# *tup1表示把tup1这个list的所有元素作为可变参数传进去
# 可变参数把传入的任意个参数自动组装为一个tuple

print('*************************')

# 而，关键字参数把传入的任意个参数，自动组装为一个dict


def person(name, age, **kw):
    if 'city' in kw:
        pass
    if 'job' in kw:
        pass
    print('name:', name, 'age:', age, 'other:', kw)


person('li', 20)
person('meimei', 15,  hobby='music, travel')
person('john', 50, hobby='reading', city='paris')

extra = {'city': 'beijing', 'job': 'manager'}
person('feng', 40, **extra)
print(extra['city'])

# 命名关键字参数, 限制输入的关键字参数


def person1(name, age, *, city, job):
    print(name, age, city, job)


# 只接收city job
person1('liu', 33, city='chengdu', job='seller')
#person1('zhao', 35)
# TypeError: person1() missing 2 required keyword-only arguments: 'city' and 'job'

# python参数定义的顺序必须是：必选参数，默认参数，可变参数，命名关键字参数和关键字参数
# positional arguments, keyword-only argument


def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)


def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


f1(13, 23, 4, (1,2,3), city='shanghai')
f1(*(1,2,3,(1,2)), city='shanghai')
f1(1,2,3,'a','bc',xy=100)
print('*************************')
f2(33,22,d=100,job='mgr')

args2 = (1,2)
f2(*args2, d=100, city='bj')
kw2 = {'d': 100, 'city': 'bj'}
f2(*args2, **kw2)

# *args是可变参数，接收的是一个tuple ()
# **kw是关键字参数，接收的是一个dict {}

print('*************************')

# 递归函数--函数在内部调用自己
# 计算n! = 1x2x3x...xn


def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)


print(fact(5))

# 尾递归，在函数返回的时候，调用自身，并且，return语句不能包含表达式。
# 这样，编译器可以把尾递归作优化，使得递归本身无论被调用多少次，都只占用一个栈帧，避免出现栈溢出。
# 然而，python的解释器没有做优化，还是会溢出。大多数编程语言都没有针对尾递归优化。


def fact1(n):
    return fact_iter(n, 1)


def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)
# 上面的returnbaohan了自身，单没有表达式

print(fact1(1000))
