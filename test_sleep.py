#!/usr/bin/env python

import time

baseline = time.time()
SLEEP_TIME = 10
print "(%f) About to call sleep for %d seconds" % ( time.time()-baseline, SLEEP_TIME )
time.sleep(SLEEP_TIME)
print "(%f) Wake ups" % (time.time()-baseline)

