#####################################################
# This version assumes the 3-way pinch valve design
#####################################################

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
        # Chan 0: Left odor pinch valve 1
        # Chan 1  Left odor pinch valve 2
        # Chan 2: Right odor pinch valve 1 
        # Chan 3: Right odor pinch valve 2
        # Chan 4: Left 3-way
        # Chan 5: Right 3-way
        # Chan 6: 2p external trigger
        # Chan 7: 2p wide field olfactometer trigger
        self.dio_chans = []
        for i in range(8):
            chan = subdev.channel(i, factory=DigitalChannel)
            chan.dio_config(IO_DIRECTION.output)
            self.dio_chans.append( chan )       

        self.pv_s = [ 0, 0, 0, 0 ]

        self.reset_all()

    def activate_2p_olfactometer_trigger(self):
        self.dio_chans[ 7 ].dio_write( 1 )

    def deactivate_2p_olfactometer_trigger(self):
        self.dio_chans[ 7 ].dio_write( 0 )

    def activate_2p_external_trigger(self):
        self.dio_chans[ 6 ].dio_write( 1 )

    def deactivate_2p_external_trigger(self):
        self.dio_chans[ 6 ].dio_write( 0 )

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
        
        # Assumes the 3-way pinch valves 
        # have air by default
        if valve_state_str == 'Both_Air' or \
           valve_state_str == 'Both_Air_Rev' or \
           valve_state_str == 'Left_Air' or \
           valve_state_str == 'Left_Air_Rev' or \
           valve_state_str == 'Right_Air' or \
           valve_state_str == 'Right_Air_Rev': 
            self.pv_s = [ 0, 0, 0, 0 ]
        elif valve_state_str == 'Both_Odor':
            self.pv_s = [ 1, 1, 1, 1 ]
        elif valve_state_str == 'Right_Odor':
            # self.pv_s = [ 0, 0, 1, 1 ]
            # Everything is going through the left air flow track
            self.pv_s = [ 1, 1, 0, 0 ]
        elif valve_state_str == 'Left_Odor':  
            self.pv_s = [ 1, 1, 0, 0 ]
        else:
            print "ERROR: valve_state_str not recognized: ", valve_state_str        
        
        # Send signals to daq board
        for i, s in enumerate(self.pv_s):
            self.dio_chans[ i ].dio_write( s )
            
        print "(%f): Activated pinch valves to: %s" % (time.time()-self.start_t, valve_state_str)

    def close(self):
        self.daq_s.close()
        
    def reset_all(self):
        
        self.deactivate_2p_external_trigger()
        self.deactivate_3way_valves()
        self.deactivate_2p_olfactometer_trigger()
    
        # deactivate dio channels
        self.pv_s = [ 0, 0, 0, 0 ]
        
        for i, s in enumerate(self.pv_s):
            self.dio_chans[ i ].dio_write( s )
