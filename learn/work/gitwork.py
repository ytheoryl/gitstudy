#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# os.system('mysql -uroot -p654321 < check.sql > checkresult.txt')
'''
content of check.sql:
show databases;
use zabbix;
show tables;
select * from graphs;
select * from graphs_items;
select * from graphs where grapshid=541;
exit

filesql = open('root/checkresult.txt')
print(filesql.read())
filesql.close()
'''

shpath = '/home/leo/github/gitest/learn/work'
os.system('%s/gitsteps.sh > %s/gitstepsresult.txt' % (shpath, shpath))

filesh = open('%s/gitstepsresult.txt' % shpath, 'r')
abc = filesh.read()
filesh.close()

with open('%s/file1.txt' % shpath, 'w') as file1
    file1.write(abc)


# git daily steps
