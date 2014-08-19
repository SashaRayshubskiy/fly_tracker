import time
import Queue
import threading

from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue

class FlyBallPlotterContinuous:
    def __init__(self, data_q, geometry, central_widget):
        
        self.data_q = data_q

        # Setup plot area
        self.plot_area = QWidget( central_widget )
        self.plot_area.setGeometry( geometry )
        self.dpi = 100
        self.fig = Figure( dpi=self.dpi )
        self.canvas = FigureCanvas( self.fig )
        self.canvas.setParent( self.plot_area )

        self.axes = self.fig.add_subplot(111)

        # Setup update timer
        self.update_freq = 10
        self.timer = QTimer()
        self.timer.timeout.connect( self.updatePlot )
        self.timer.start( 1000.0 / self.update_freq )

    def updatePlot(self):
        
        # Read data from queue
        qdata = list(get_all_from_queue(self.data_q))

        t, dx, dy = zip(*qdata)

        # plot data
        self.axes.plot(dx,dy,hold=True)
        

class FlyBallReaderThread(threading.Thread):
    def __init__(self, data_q, trial_data_q, trial_ball_data_acq_start_event):
        threading.Thread.__init__(self)
        
        self.data_q = data_q
        self.trial_data_q = trial_data_q
        self.trial_ball_data_acq_start_event = trial_ball_data_acq_start_event

        self.mouse = file('/dev/input/mouse1')

        self.start()

    def to_signed(self, n):
        return n - ((0x80 & n) << 1)

    def run(self):        

        time.clock()

        while True:
            status, dx, dy = tuple(ord(c) for c in self.mouse.read(3))
                        
            t = time.clock()
            dx = self.to_signed(dx)
            dy = self.to_signed(dy)
            
            self.data_q.put((t,dx,dy))
            
            if self.trial_ball_data_acq_start_event.isSet():
                self.trial_data_q.put((t,dx,dy)) 
            # print "%#02x %d %d" % (status, dx, dy)            
                
        
