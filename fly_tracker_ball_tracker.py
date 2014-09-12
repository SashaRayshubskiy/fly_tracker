import numpy as np
import math
import time
import Queue
import threading
import scipy.io
from datetime import datetime

from PyQt5.QtWidgets import  QWidget
from PyQt5.QtCore import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from fly_tracker_utils import get_all_from_queue

class FlyBallPlotterContinuous:
    def __init__(self, data_q, geometry, central_widget, experiment_dir):
        
        self.data_q = data_q
        self.experiment_dir = experiment_dir

        # Setup plot area
        self.plot_area = QWidget( central_widget )    
        self.plot_area.setGeometry( geometry )
        w = geometry.width()
        h = geometry.height()
        self.dpi = 80
        
        w_inch = math.ceil(float(w) / float(self.dpi)) 
        h_inch = math.ceil(float(h) / float(self.dpi))

        # print "ball_tracker: w_inch, h_inch: ( %f %f )" % ( w_inch, h_inch )
        # print "ball_tracker: w, h: ( %f %f )" % ( w, h )

        self.fig = Figure( figsize=(4, 4), dpi=self.dpi, facecolor="w" )        
        self.canvas = FigureCanvas( self.fig )
        self.canvas.setParent( self.plot_area )

        self.axes = self.fig.add_subplot(111)
                
        # Setup update timer
        self.update_freq = 20
        self.timer = QTimer()
        self.timer.timeout.connect( self.updatePlot )
        self.timer.start( 1000.0 / self.update_freq )

        # 
        self.cur_traj_x = 0
        self.cur_traj_y = 0        

        self.t_all = np.zeros(0)
        self.dx_all = np.zeros(0)
        self.dy_all = np.zeros(0)
        self.FORMAT = '%Y_%m%d_%H%M%S'
        self.RAWDATA_FLUSH_THRESHOLD = 100000000

    def save_raw(self):
        if self.experiment_dir is not None:        
            datapathbase =  self.experiment_dir + '/' + datetime.now().strftime( self.FORMAT )
            save_d = {}
            save_d['t_all'] = self.t_all
            save_d['dx_all'] = self.dx_all
            save_d['dy_all'] = self.dy_all
            # print "size of self.t_all: ", self.t_all.shape[0]
            # print "size of self.dx_all: ", self.dx_all.shape[0]
            # print "size of self.dy_all: ", self.dy_all.shape[0]
            scipy.io.savemat( datapathbase + '_raw_cummulative_xy.mat', save_d )

    def close(self):
        if self.experiment_dir is not None:
            datapathbase =  self.experiment_dir + '/' + datetime.now().strftime( self.FORMAT )
            self.fig.savefig( datapathbase + '_cummulative_xy.eps', format='eps', dpi=1000, bbox_inches='tight')
            self.fig.savefig( datapathbase + '_cummulative_xy.png', format='png', dpi=1000, bbox_inches='tight')
            
            self.save_raw()

    def updatePlot(self):
        
        # Read data from queue
        qdata = list(get_all_from_queue(self.data_q))

        if len(qdata) > 0:
            t, dx, dy = zip(*qdata)

            # Save the data for later output
            self.t_all = np.append(self.t_all, t)
            self.dx_all = np.append(self.dx_all, dx)
            self.dy_all = np.append(self.dy_all, dy)            

            if self.t_all.shape[0] > self.RAWDATA_FLUSH_THRESHOLD:
                self.save_raw()
                self.t_all = np.zeros(0)
                self.dx_all = np.zeros(0)
                self.dy_all = np.zeros(0)

            # Calculate trajectory
            i=0
            traj_x = np.zeros( len(dx) )
            traj_y = np.zeros( len(dy) )
            while i<len(dx):
                if i == 0:
                    traj_x[i] = self.cur_traj_x + dx[i]
                    traj_y[i] = self.cur_traj_y + dy[i]
                else:
                    traj_x[i] = traj_x[i-1] + dx[i]
                    traj_y[i] = traj_y[i-1] + dy[i]
                i=i+1

            self.cur_traj_x = traj_x[ -1 ]
            self.cur_traj_y = traj_y[ -1 ]

            # plot data        
            self.axes.hold( True )
            # self.axes.plot( dx, dy, color='b' )
            self.axes.plot(traj_x,traj_y, color='b')
            self.fig.canvas.draw()

class FlyBallReaderThread(threading.Thread):
    def __init__(self, data_q, trial_data_q, trial_ball_data_acq_start_event):
        threading.Thread.__init__(self)
        
        self.data_q = data_q
        self.trial_data_q = trial_data_q
        self.trial_ball_data_acq_start_event = trial_ball_data_acq_start_event

        self.mouse = file('/dev/input/mouse0')

        self.setDaemon(True)
        self.start()

    def to_signed(self, n):
        return n - ((0x80 & n) << 1)

    def run(self):        

        while True:
            status, dx, dy = tuple(ord(c) for c in self.mouse.read(3))
                        
            t = time.time()
            
            # x+ => right, x- => left
            dx = self.to_signed(dx)
            
            # y+ => backward, y- => forward
            # reverse the sign to make y+ => forward
            dy = -1 * self.to_signed(dy)
            # print "FlyBallReaderThread: ( %f %d %d )" % ( t, dx, dy )
            self.data_q.put((t,dx,dy))
            
            if self.trial_ball_data_acq_start_event.isSet():
                self.trial_data_q.put((t,dx,dy)) 
            # print "%#02x %d %d" % (status, dx, dy)            
                
        
