#!/var/bin/env python3
# -*- coding:utf-8 -*-

score = {'michael': 95, 'bob': 80, 'leo': 100}
print(score['leo'])

# add a new key to end of the dict
score['jack'] = 99
score['wang'] = 94
print(score)

# change a value
score['leo'] = 98
print(score['leo'])

print('thomas' in score)  # to check if thomas in the dict
print(score.get('thomas'))  # to get the value of key which doesn't exist. retuen none
print(score.get('thomas', 'not found'))  # specify a return value if doesn't exist

score.pop('michael')  # delete a key
print(score)

# a tuple can be key in dict, but list cannot. [1, 2, 3] cannot by key name since key cannot change.
keya = (1, 2, 3)
score[keya] = 'a tuple'
# but a list can be the value
yoho = [1, 2, 3]
score['yoho'] = yoho
print(score)

print('********************************************************')

sili = set([1, 2, 2, 2, 3, 3])
print(sili)
sili.add(4)
sili.add(4)
sili.add(3)
print(sili)

soho = set()
soho.add(1)
soho.add(5)
soho.add(4)
soho.add(3)
soho.add(5)
soho.remove(1)
print(soho)

print('********************************************************')

# find the common keys
print(soho & sili)  # 求交集
print(sili | soho)  # 求并集

print('********************************************************')

# a list can be changed, but others cannot
biao = ['bravo', 'charlie', 'daff', 'apple']
biao.sort()
print(biao)

book = 'abcd'
book.replace('a', 'X')
print(book)

print('********************************************************')


def scores(**kw):
    print('    name  score')
    print('-------------------')
    for name, score in kw.items():
        print('%10s   %d' % (name, score))
    print()


scores(adam=99, lisa=88, bart=77)
print('***************')

dicta = {'ibm':1,'hp':2,'intel':3}
for x, y in dicta.items():
    print(y, x)
