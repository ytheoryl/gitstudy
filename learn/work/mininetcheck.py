#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#to check the mininet hosts and switches number. ~/mininet/example/tree1024.py
"""
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
from mininet.topolib import TreeNet

if __name__ == '__main__':
    setLogLevel( 'info' )
    network = TreeNet( depth=3, fanout=4, switch=OVSSwitch )
    network.run( CLI, network )
"""

import math

depth = int(input('What\'s the depth of your topology:'))
fanout = int(input('What\s the fanout of your tolology:'))

host = fanout ** depth
switch = (depth-1)*fanout+1

print('You have %i switches and %i hosts.' % (switch, host))
