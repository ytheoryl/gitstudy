#-*- coding;utf-8 -*-

import re

text = """
12    <HIST> IPC-ATCA100            OMU-0       SWITCH    2017-11-09  07:36:39.71
    NOTICE VTP-20                            IOMANA
    (9428) 0690 WORKING STATE CHANGE

3 ok	< ZAHP:::;

LOADING PROGRAM VERSION 6.14-0
4 ok < DDE:MCHU,0:"ZTOP:O;",;

LOADING PROGRAM VERSION 8.26-0

Flexi NS  SHMME06BNK                2017-11-10  05:47:44

WELCOME TO SERVICE TERMINAL DIALOGUE

5 0004-MAN> ZTOP:O;
MCHU-0    WOEX             N7 5.17-4

6 HIST> IPC-

"""


#  (?<!(TOO|MAN|SYS|IST))[>#<?](?!\s(IPC|ZTOP))

check = re.compile('(?<!(TOO|MAN|SYS|IST))[>#<?](?!\sZTOP)')

result = check.finditer(text)
for m in result:
    print (m.group())

