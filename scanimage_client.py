import socket
import time
import sys

class SI_Client:
    def __init__( self ):
        
        self.PORT = 30000
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('10.11.176.41', self.PORT))
        time.sleep(1.0)

    def send( self, data_str ):
        self.sock.sendall( data_str + '\n' )

    def disconnect(self):
        self.sock.close()
