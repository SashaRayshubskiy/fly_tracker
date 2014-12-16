#!/usr/bin/env python

import time
import sys
import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('10.11.176.41', 30000))
time.sleep(1)
d = clientsocket.send('hello_matlab\n')
print d
# time.sleep(3)
clientsocket.close()
