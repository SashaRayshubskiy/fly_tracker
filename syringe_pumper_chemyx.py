# Serial port for syringe pump communication
import time
import serial
import struct

class SyringePumper:
    
    debug = True
    INFUSE = 1
    WITHDRAW = 2
    

    def __init__(self, start_t, syringe_size, prate):      

        self.start_t = start_t
        self.syringe_size = syringe_size

        self.direction = self.INFUSE

        # Connect to serial port for syringe pump control
        self.ser_s = serial.Serial('/dev/ttyS0', baudrate=38400)
    
        # Set the appropriete syringe pump defaults
        self.set_syringe_size(self.syringe_size)
        self.set_rate(prate)
        self.withdraw()

    def get_max_rate(self):
        if self.syringe_size == 30.0:
            return 36.0
        elif self.syringe_size == 50.0:
            return 56.0
        elif self.syringe_size == 60.0:
            return 56.0
        else:
            print "ERROR: Please set max rate for syringe volume: " % (self.syringe_vol)

    def write_to_serial_sock(self, str):
        self.ser_s.write(str + "\r")
        time.sleep(0.3)
        self.ser_s.flush()
        self.ser_s.flushInput()
        self.ser_s.flushOutput()
                
    def infuse(self):
        if self.debug: 
            print "(%f): called infuse" % (time.time()-self.start_t)
        self.write_to_serial_sock("set volume 30.0")
        #self.direction = self.INFUSE

    def withdraw(self):
        if self.debug: 
            print "(%f): called withdraw" % (time.time()-self.start_t)
        self.write_to_serial_sock("set volume -30.0")
        #self.direction = self.WITHDRAW

    def start(self):
        t0 = time.time()
        if self.debug: 
            print "(%f): called start" % (time.time()-self.start_t)
        self.write_to_serial_sock("start")
        t1 = time.time()
        return t1-t0

    def stop(self):
        if self.debug: 
            print "(%f): called stop" % (time.time()-self.start_t)
        self.write_to_serial_sock("stop")

    """
    def set_volume(self, volume):
        if self.debug: 
            print "(%f): called set_volume (%f)" % (time.time()-self.start_t, volume)

        dir_sign = None
        if self.direction == self.WITHDRAW:
            dir_sign = -1
        elif self.direction == self.INFUSE:
            dir_sign = 1

        d_str = "set volume %2.1f" % ( dir_sign * volume )
        self.write_to_serial_sock(d_str)
    """

    def set_rate(self, rate):
        if self.debug: 
            print "(%f): called set_rate (%f)" % (time.time()-self.start_t, rate)

        d_str = "set rate %2.1f" % ( rate )
        self.write_to_serial_sock(d_str)

    def get_diameter(self, syringe_size):
        diameter = -1
        if syringe_size == 10.0:
            diameter = 14.5
        elif syringe_size == 20.0:
            diameter = 19.13
        elif syringe_size == 30.0:
            diameter = 21.69
        elif syringe_size == 50.0:
            diameter = 28.03
        elif syringe_size == 60.0:
            diameter = 26.72
        else:
            print "ERROR: set syringe size to diameter mapping for size: %f" % ( syringe_size )
      
        return diameter        

    def set_syringe_size(self, syringe_size):
        if self.debug: 
            print "(%f): called set_diameter" % (time.time()-self.start_t)

        self.syringe_size = syringe_size

        self.syringe_diameter = self.get_diameter( self.syringe_size )
        print "self.syringe_diameter: ", self.syringe_diameter

        self.write_to_serial_sock("set diameter %2.2f" % (self.syringe_diameter))
        
    def close(self):
        if self.debug: 
            print "(%f): called close" % (time.time()-self.start_t)
        self.ser_s.close()
        
    def reset(self):
        if self.debug: 
            print "(%f): called reset: NO RESET command for these pumps" % (time.time()-self.start_t)

    def set_addr(self, addr):
        if self.debug: 
            print "(%f): called set_addr: NO SET ADDR command for these pumps" % (time.time()-self.start_t)
        
