#!/usr/bin/env python

import time
import sys

from daq_rider_optostim import *

dr = DAQRider(time.time())
#dr.activate_2p_olfactometer_trigger()
#dr.activate_2p_external_trigger()
#dr.activate_pinch_valves(sys.argv[1])
#dr.activate_3way_valve_left()
#dr.activate_3way_valves()
#time.sleep(3)
command = sys.argv[1]

if command  == 'Left':
    dr.activate_3way_valve_left()
elif command == 'Right':
    dr.activate_3way_valve_right()
elif command == 'Both':
    dr.activate_3way_valves()
elif command == 'Close':
    dr.deactivate_3way_valves()
elif command == 'On':
    dr.activate_pinch_valves(sys.argv[2])
elif command == 'WideFieldBlueOn':
    dr.activate_widefield_blue_led_channel()
elif command == 'WideFieldBlueOff':
    dr.deactivate_widefield_blue_led_channel()
elif command == 'Off':
    dr.deactivate_pinch_valves()
elif command == 'Activate2p':
    dr.activate_2p_external_trigger()
elif command == 'Deactivate2p':
    dr.deactivate_2p_external_trigger()

time.sleep( 3 )
dr.reset_all()
dr.close()
