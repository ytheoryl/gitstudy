#!/var/bin/env python3
# -*- coding: utf-8 -*-

import os
from learn.privatelib import exec_shell

print('file and directory operation')
hostip = '192.168'
hostname = 'NBG'
hosttype = 'ibm'
hostpath = '/home/leo/Documents'
# hostfile means /home/leo/Documents/cpu_192.168_NBG_ibm.txt
hostfile = os.path.join(hostpath, 'cpucpu_%s_%s_%s.txt' % (hostip, hostname, hosttype))
print(hostfile)

os.system('cat /proc/cpuinfo | grep model > %s' % hostfile)
run = exec_shell('cat %s' % hostfile)
print(run)
exec_shell('echo "" > %s' % hostfile)
