#!/usr/bin/env python

import time
import sys
from daq_rider_v2 import *

dr = DAQRider(time.time())
#dr.activate_2p_olfactometer_trigger()
#dr.activate_2p_external_trigger()
#dr0.activate_pinch_valves(sys.argv[1])
#dr.activate_3way_valve_left()
#dr.activate_3way_valves()
#time.sleep(3)
#dr.reset_all()
command = sys.argv[1]

if command  == 'Left':
    dr.activate_3way_valve_left()
elif command == 'Right':
    dr.activate_3way_valve_right()
elif command == 'Both':
    dr.activate_3way_valves()
elif command == 'Close':
    dr.deactivate_3way_valves()

dr.close()
