#!/usr/bin/env python

import time
import sys
from daq_rider import *

dr = DAQRider(time.time())

#dr.activate_pinch_valves(sys.argv[1])
#time.sleep(3)
dr.activate_3way_valves_left()
time.sleep(3)
dr.reset_all()
dr.deactivate_3way_valves()
dr.close()
