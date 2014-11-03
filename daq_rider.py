# DAQ board communication
import sys
import time
from pycomedi.device import Device
from pycomedi.channel import DigitalChannel
from pycomedi.constant import SUBDEVICE_TYPE, AREF, UNIT, IO_DIRECTION

class DAQRider:
    def __init__(self, start_t):
        
        self.start_t = start_t

        # Connect to DAQ board
        self.daq_s = Device('/dev/comedi0')
        self.daq_s.open()
        subdev = self.daq_s.find_subdevice_by_type(SUBDEVICE_TYPE.dio)

        # Create 6 channels: 4 pinch valves and 2 3-way valves
        # Right/Left from perspective of the fly's face looking straight
        # Chan 0: Right Odor pinch valve
        # Chan 1: Left Air pinch valve 
        # Chan 2: Right Air pinch valve
        # Chan 3: Left Odor pinch valve
        # Chan 4: Left 3-way
        # Chan 5: Right 3-way
        self.dio_chans = []
        for i in range(6):
            chan = subdev.channel(i, factory=DigitalChannel)
            chan.dio_config(IO_DIRECTION.output)
            self.dio_chans.append( chan )       

        self.pv_s = [ 0, 0, 0, 0 ]

        self.reset_all()        

    def deactivate_3way_valves(self):
        self.dio_chans[ 4 ].dio_write( 0 )
        self.dio_chans[ 5 ].dio_write( 0 )

    def activate_3way_valve_left(self):
        self.dio_chans[ 4 ].dio_write( 1 )

    def activate_3way_valve_right(self):
        self.dio_chans[ 5 ].dio_write( 1 )

    def activate_3way_valves(self):
        self.activate_3way_valve_right()
        self.activate_3way_valve_left()

    def activate_pinch_valves(self, valve_state_str):
        
        if valve_state_str == 'Both_Air': 
            self.pv_s = [ 0, 1, 1, 0 ]
        elif valve_state_str == 'Both_Odor':
            self.pv_s = [ 1, 0, 0, 1 ]
        elif valve_state_str == 'Right_Odor':
            self.pv_s = [ 1, 1, 0, 0 ]
        elif valve_state_str == 'Left_Odor':  
            self.pv_s = [ 0, 0, 1, 1 ]
        elif valve_state_str == 'Left_Air':  
            self.pv_s = [ 0, 1, 0, 0 ]
        elif valve_state_str == 'Right_Air':  
            self.pv_s = [ 0, 0, 1, 0 ]
        else:
            print "ERROR: valve_state_str not recognized: ", valve_state_str        
        
        # Send signals to daq board
        for i, s in enumerate(self.pv_s):
            self.dio_chans[ i ].dio_write( s )
            
        print "(%f): Activated pinch valves to: %s" % (time.time()-self.start_t, valve_state_str)

    def close(self):
        self.daq_s.close()
        
    def reset_all(self):
        
        self.deactivate_3way_valves()
    
        # deactivate dio channels
        self.pv_s = [ 0, 0, 0, 0 ]
        
        for i, s in enumerate(self.pv_s):
            self.dio_chans[ i ].dio_write( s )
