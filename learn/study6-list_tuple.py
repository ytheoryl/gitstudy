# -*- coding: utf-8 -*-
line = '+++++++++++++++++++++++++++++++++++++++'

laptop = ['sony', 'ibm', 'hp', 'dell', 'apple']
print(len(laptop), laptop)
print('I like %s thinkpad! :)' % laptop[1])
print('But I don\'t like %s xps :(' % laptop[-2])
print(line)

laptop.append('compaq')  # append one element to last position
laptop.insert(3, 'lenovo')  # insert to the designated position
print(laptop)
laptop.pop()  # delete the last one
print(laptop)
laptop.pop(3)  # delete the designated position
print(laptop)
laptop[0] = 'asus'  # replace [0] with new value
print(laptop)

print(line)

bag = ['iphone', 7, True, laptop]  # a list can store data of different types
print(len(bag), bag)
print('%s%d is a product from %s: %s' % (bag[0], bag[1], bag[3][-1], bag[2]))  # bag是一个二维数组

print(line)

game = ('doom', 'diablo', 23, laptop)
print(game)
game[3][0] = 'compaq'
print(game)

one = (1)
specialone = (1,)  # , is mandatory to define a tuple with element 1
print(one, 'is not a tuple.', specialone, 'is a tuple')
