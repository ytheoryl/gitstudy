#!/var/bin/env python3
# -*- coding: utf-8 -*-


def info(name, *, gender, city='beijing', age):
    print('Personal Info')
    print('----------------')
    print('    Name: %s' % name)
    print('%9s %s' % ('Gender:', gender))
    print('    City: %s' % city)
    print('     Age: %s' % age)
    print()


info('bob', gender='male', age=20)


args = ('ag', 'be', 'cs')
print('%s, %s!' % ('hello', ','.join(args)))
print('%s, %s!' % ('hello', ', '.join(args)))
