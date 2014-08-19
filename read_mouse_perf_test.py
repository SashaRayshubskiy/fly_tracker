#!/usr/bin/env python

import sys
import timeit

NUM_ITERS=1000
t = timeit.timeit('status, dx, dy = tuple(ord(c) for c in mouse.read(3))', setup='mouse=file(\'/dev/input/mouse1\')', number=NUM_ITERS)

print 'Speed: ' + str(float(NUM_ITERS) / t)


"""
mouse = file('/dev/input/mouse1')

while True:
    status, dx, dy = tuple(ord(c) for c in mouse.read(3))
 
    def to_signed(n):
        return n - ((0x80 & n) << 1)
        
    dx = to_signed(dx)
    dy = to_signed(dy)
    print "%#02x %d %d" % (status, dx, dy)
"""
