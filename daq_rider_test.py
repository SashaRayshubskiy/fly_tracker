#!/usr/bin/env python

import time
import sys
from daq_rider import *

dr = DAQRider(time.time())
#dr.activate_pinch_valves(sys.argv[1])
dr.activate_3way_valves()
time.sleep(4)
#dr.reset_all()
dr.deactivate_3way_valves()
dr.close()
