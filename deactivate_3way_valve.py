#!/usr/bin/env python

import time
import sys
from daq_rider import *

dr = DAQRider(time.time())
dr.deactivate_3way_valves()
dr.close()
