#!/usr/bin/env python

import timeit

NUMBER_ITERS=1000
t = timeit.timeit('status, dx, dy = tuple(ord(c) for c in mouse.read(3))', setup='mouse = file(\'/dev/input/mouse0\')', number=NUMBER_ITERS)
print "Mouse read performance: %f Hz" % (float(NUMBER_ITERS)/t)

