# Serial port for syringe pump communication
import time
import serial
import struct

class SyringePumper:
    
    debug = True
    
    def __init__(self, start_t, diameter, prate):      

        self.start_t = start_t

        # Connect to serial port for syringe pump control
        self.ser_s = serial.Serial('/dev/ttyS0', baudrate=19200)

        # Set the appropriete syringe pump defaults
        self.write_to_serial_sock("LN 1")
        self.set_rate(prate)
        self.set_diameter(diameter)
        self.withdraw()

    def write_to_serial_sock(self, str):
        self.ser_s.write(str + "\r")
        time.sleep(0.1)
        self.ser_s.flush()
        self.ser_s.flushInput()
        self.ser_s.flushOutput()
        
        #self.process_serial_response()

    def process_serial_response(self):
        
        STX=0x02
        ETX=0x03

        # Read till 
        bytes_read_till_start = 0
        cur_byte_as_int = -1
        while True:

            cur_byte_as_int = ord(self.ser_s.read(size=1))
            print "Collecting start:: cur_byte_as_int: %d" % (cur_byte_as_int)
            bytes_read_till_start = bytes_read_till_start + 1

            if cur_byte_as_int == STX:
                break
                            
            if bytes_read_till_start % 100 == 0:
                print "WARNING:: Not finding the start of the serial port response"
        
        print "bytes_read_till_start: ", bytes_read_till_start
        print "cur_byte_as_int: ", cur_byte_as_int

        # Collect the response 
        response = []
        while True:
            cur_byte = ord(self.ser_s.read(size=1))
            print "Collecting response:: cur_byte: %d, char: %s" % (cur_byte, str(unichr(cur_byte)))
            
            response.append(cur_byte)

            if cur_byte == ETX:
                # End of message
                break

        if len(response) < 2:
            print "ERROR: insufficient response: ", response

        # Process the response protocol for received message
        
        response_c = [str(unichr(cc)) for cc in response]
        print "Response: ", response_c

        address1 = response[ 0 ]        
        address2 = response[ 1 ]
        
        status = response[2]
        
        print "(%f): Address: %s status: %s" % (time.time()-self.start_t, str(unichr(address1)), str(unichr(status)))

        if status == ord('S'):
            self.ser_s.flushOutput()
            self.ser_s.flushInput()
        
    def infuse(self):
        if self.debug: 
            print "(%f): called infuse" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 DIR INF * 2 DIR INF *")

    def withdraw(self):
        if self.debug: 
            print "(%f): called withdraw" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 DIR WDR * 2 DIR WDR *")

    def start(self):
        if self.debug: 
            print "(%f): called start" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 RUN * 2 RUN *")

    def start_left(self):
        if self.debug: 
            print "(%f): called start" % (time.time()-self.start_t)
        self.write_to_serial_sock("2 RUN")

    def start_right(self):
        if self.debug: 
            print "(%f): called start" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 RUN *")

    def stop(self):
        if self.debug: 
            print "(%f): called stop" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 STP * 2 STP *")

    def stop_left(self):
        if self.debug: 
            print "(%f): called stop" % (time.time()-self.start_t)
        self.write_to_serial_sock("2 STP *")

    def stop_right(self):
        if self.debug: 
            print "(%f): called stop" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 STP *")

    def set_rate(self, rate):
        if self.debug: 
            print "(%f): called set_rate (%f)" % (time.time()-self.start_t, rate)

        d_str = "1 RAT %2.1f MM * 2 RAT %2.1f MM *" % (rate, rate);
        print "set_rate command: %s" % (d_str) 
        self.write_to_serial_sock(d_str)

    def set_diameter(self, diameter):
        if self.debug: 
            print "(%f): called set_diameter" % (time.time()-self.start_t)
        self.write_to_serial_sock("1 DIA %2.2f * 2 DIA %2.2f *" % (diameter, diameter))
        
    def close(self):
        if self.debug: 
            print "(%f): called close" % (time.time()-self.start_t)
        self.ser_s.close()
        
    def reset(self):
        if self.debug: 
            print "(%f): called reset" % (time.time()-self.start_t)
        self.write_to_serial_sock("*RESET")

    def set_addr(self, addr):
        if self.debug: 
            print "(%f): called set_addr" % (time.time()-self.start_t)
        self.write_to_serial_sock("*ADR %d" % (addr))
        
