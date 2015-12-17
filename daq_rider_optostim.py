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
        # Chan 0: Microscope wide-field blue LED 
        # Chan 1  Left odor LED
        # Chan 2: Right odor LED
        # Chan 3: Free
        # Chan 4: Free
        # Chan 5: Free
        # Chan 6: 2p external trigger
        # Chan 7: 2p wide field olfactometer trigger
        self.dio_chans = []
        for i in range(8):
            chan = subdev.channel(i, factory=DigitalChannel)
            chan.dio_config(IO_DIRECTION.output)
            self.dio_chans.append( chan )       

        self.pv_s = [ 0, 0 ]

        self.SIMPLE_ODOR_VALVE_CHANNEL = 3
        self.BLUE_LED_CHANNEL = 2

        self.reset_all()

    def activate_widefield_blue_led_channel(self):
        self.dio_chans[ self.BLUE_LED_CHANNEL ].dio_write( 1 )

    def deactivate_widefield_blue_led_channel(self):
        self.dio_chans[ self.BLUE_LED_CHANNEL ].dio_write( 0 )

    def activate_simple_odor_valve_channel(self):
        self.dio_chans[ self.SIMPLE_ODOR_VALVE_CHANNEL ].dio_write( 1 )

    def deactivate_simple_odor_valve_channel(self):
        self.dio_chans[ self.SIMPLE_ODOR_VALVE_CHANNEL ].dio_write( 0 )

    def activate_2p_olfactometer_trigger(self):
        self.dio_chans[ 7 ].dio_write( 1 )

    def deactivate_2p_olfactometer_trigger(self):
        self.dio_chans[ 7 ].dio_write( 0 )

    def activate_2p_external_trigger(self):
        self.dio_chans[ 6 ].dio_write( 1 )

    def deactivate_2p_external_trigger(self):
        self.dio_chans[ 6 ].dio_write( 0 )

    def activate_pinch_valves(self, valve_state_str):
        
        if valve_state_str == 'Both_Odor':
            self.pv_s = [ 1, 1 ]
        elif valve_state_str == 'Right_Odor':
            self.pv_s = [ 1, 0 ]
        elif valve_state_str == 'Left_Odor':  
            self.pv_s = [ 0, 1 ]
        else:
            print "ERROR: valve_state_str not recognized: ", valve_state_str        
        
        # Send signals to daq board
        for i, s in enumerate(self.pv_s):
            self.dio_chans[ i ].dio_write( s )
            
        print "(%f): Activated pinch valves to: %s" % (time.time()-self.start_t, valve_state_str)

    def deactivate_pinch_valves(self):
        # deactivate dio channels
        self.pv_s = [ 0, 0 ]
        
        for i, s in enumerate(self.pv_s):
            self.dio_chans[ i ].dio_write( s )        

    def close(self):
        self.daq_s.close()
        
    def reset_all(self):        
        self.deactivate_2p_external_trigger()
        self.deactivate_2p_olfactometer_trigger()
        self.deactivate_pinch_valves()
        self.deactivate_widefield_blue_led_channel()
