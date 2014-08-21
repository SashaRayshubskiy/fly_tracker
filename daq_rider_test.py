#!/usr/bin/env python

import time
import sys
from daq_rider import *

dr = DAQRider(time.time())
dr.activate_pinch_valves(sys.argv[1]+' '+sys.argv[2])
time.sleep(3)
dr.reset_all()
dr.close()
