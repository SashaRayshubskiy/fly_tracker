# Serial port for syringe pump communication
import serial

class SyringePumper:
    
    def __init__(self, diameter, prate):      
        # Connect to serial port for syringe pump control
        self.ser_s = serial.Serial('/dev/ttyS0', baudrate=19200)
        # self.ser_s.open()

        # Set the appropriete syringe pump defaults
        self.set_rate(prate)
        self.set_diameter(diameter)
        self.withdraw()

    def write_to_serial_sock(self, str):
        self.ser_s.write(str + "\r")

    def infuse(self):
        self.write_to_serial_sock("1 DIR INF * 2 DIR INF *")

    def withdraw(self):
        self.write_to_serial_sock("1 DIR WDR * 2 DIR WDR *")

    def start(self):
        self.write_to_serial_sock("1 RUN * 2 RUN *")

    def stop(self):
        self.write_to_serial_sock("1 STP * 2 STP *")

    def set_rate(self, rate):
        #d_str = "1 RAT %2.2f MM RAT * 2 %2.2f MM *" % (rate, rate);
        d_str = "1 RAT %2.2f MM" % (rate)
        self.write_to_serial_sock(d_str)
        #print d_str

    def set_diameter(self, diameter):
        self.write_to_serial_sock("1 DIA %2.2f DIA * 2 %2.2f *" % (diameter, diameter))
        
    def close(self):
        self.ser_s.close()
